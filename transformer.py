from typing import Any

from clingo import ast, Number, String
from clingo.ast import AST, ASTSequence, ProgramBuilder


class LPMLNTransformer(ast.Transformer):
    '''
    Transforms LP^MLN rules to ASP with weak constraints in the 'Penalty Way'.
    Weights of soft rules are encoded via a theory term &weight/1 in the body.
    '''
    def __init__(self, options):
        self.rule_idx = 0
        self.expansion_variables = 0
        self.translate_hr = options[0].flag
        self.use_unsat = options[1].flag
        self.two_solve_calls = options[2].flag

    def visit(self, ast: AST, *args: Any, **kwargs: Any) -> AST:
        '''
        Dispatch to a visit method in a base class or visit and transform the
        children of the given AST if it is missing.
        '''
        if isinstance(ast, AST):
            attr = 'visit_' + str(ast.ast_type).replace('ASTType.', '')
            # print(ast)
            # print(attr)
            if hasattr(self, attr):
                return getattr(self, attr)(ast, *args, **kwargs)
        if isinstance(ast, ASTSequence):
            return self.visit_sequence(ast, *args, **kwargs)
        return ast.update(**self.visit_children(ast, *args, **kwargs))

    def _get_constraint_parameters(self, location: dict):
        """
        Get the correct parameters for the
        weak constraint in the conversion.
        """
        idx = ast.SymbolicTerm(location, Number(self.rule_idx))
        self.global_variables = ast.Function(location, "",
                                             self.global_variables, False)

        if self.weight == 'alpha':
            self.weight = ast.SymbolicTerm(location, String('alpha'))
            constraint_weight = ast.SymbolicTerm(location, Number(1))
            priority = Number(1)
        else:
            constraint_weight = self.weight
            priority = Number(0)
        priority = ast.SymbolicTerm(location, priority)
        return idx, constraint_weight, priority

    def _get_unsat_atoms(self, location: dict, idx):
        """
        Creates the 'unsat' and 'not unsat' atoms
        """
        unsat_arguments = [idx, self.weight, self.global_variables]

        unsat = ast.SymbolicAtom(
            ast.Function(location, "unsat", unsat_arguments, False))

        not_unsat = ast.Literal(location, ast.Sign.Negation, unsat)
        unsat = ast.Literal(location, ast.Sign.NoSign, unsat)

        return unsat, not_unsat

    def _convert_rule(self, head, body):
        """
        Converts the LPMLN rule using either the unsat atoms
        or the simplified approach without them
        """
        loc = head.location
        idx, constraint_weight, priority = self._get_constraint_parameters(loc)

        # Choice rules without bound can be skipped
        if str(head.ast_type) == 'ASTType.Aggregate':
            if head.left_guard is None and head.right_guard is None:
                return [ast.Rule(loc, head, body)]
            else:
                not_head = ast.Literal(loc, ast.Sign.Negation, head)

        else:
            not_head = ast.Literal(loc, ast.Sign.Negation, head.atom)

        # Create ASP rules
        # TODO: Better way to insert and delete items from body?

        if self.use_unsat:
            unsat, not_unsat = self._get_unsat_atoms(loc, idx)
            # Rule 1 (unsat :- Body, not Head)
            body.insert(0, not_head)
            asp_rule1 = ast.Rule(loc, unsat, body)

            # Rule 2 (Head :- Body, not unsat)
            del body[0]
            body.insert(0, not_unsat)
            asp_rule2 = ast.Rule(loc, head, body)

            # Rule 3 (weak constraint unsat)
            asp_rule3 = ast.Minimize(loc, constraint_weight, priority,
                                     [idx, self.global_variables], [unsat])
            return [asp_rule1, asp_rule2, asp_rule3]
        else:
            asp_rules = []
            # Choice rules with bounds, e.g. 'w : { a; b } = 1 :- B.'
            # get converted to two rules:
            # w : { a ; b } :- B.       --> { a ; b } :- B.
            # w : :- not { a ; b } = 1. --> :~ B, not {a ; b} = 1. [w,id, X]
            if str(head.ast_type) == 'ASTType.Aggregate':
                agg1 = ast.Aggregate(loc, None, head.elements, None)
                asp_rules.append(ast.Rule(loc, agg1, body))
                body.insert(0, not_head)
            # Convert integrity constraint 'w: #false :- B.' to weak constraint
            # of form: ':~ B. [w, idx, X]'
            elif str(head.atom.ast_type
                     ) == 'ASTType.BooleanConstant' and not head.atom.value:
                pass
            # Convert normal rule 'w: H :- B.' to choice rule and weak
            # constraint of form: '{H} :- B.' and ':~ B, not H. [w, idx, X]'
            else:
                cond_head = ast.ConditionalLiteral(loc, head, [])
                choice_head = ast.Aggregate(loc, None, [cond_head], None)
                asp_rules.append(ast.Rule(loc, choice_head, body))
                body.insert(0, not_head)

            if self.two_solve_calls and str(priority) == '0':
                ext_helper_atom = ast.SymbolicAtom(
                    ast.Function(loc, 'ext_helper', [], False))
                ext_helper_atom = ast.Literal(loc, ast.Sign.NoSign,
                                              ext_helper_atom)
                body.insert(0, ext_helper_atom)

            weak_constraint = ast.Minimize(loc, constraint_weight, priority,
                                           [idx, self.global_variables], body)
            asp_rules.append(weak_constraint)
            return asp_rules

    def visit_Rule(self, rule: AST, builder: ProgramBuilder):
        """
        Visits an LP^MLN rule, converts it to three ASP rules
        if necessary and adds the result to the program builder.
        """
        # Set weight to alpha by default
        self.weight = 'alpha'
        self.global_variables = []
        # self.expansions_in_body = []  # TODO: Better name, better method?

        # print('\n LP^MLN Rule')
        # print(rule)
        head = rule.head
        body = rule.body

        # Traverse head and body to look for weights and variables
        head = self.visit(head)
        body = self.visit(body)

        # # Add pools/intervals that are bound to a variable to the body
        # for e in self.expansions_in_body:
        #     body.insert(0, e)

        # print(repr(body))
        # print(self.global_variables)
        # print(self.weight)

        if self.weight == 'alpha' and not self.translate_hr:
            self.rule_idx += 1
            return rule
            # builder.add(ast.Rule(rule.location, head, body))
        else:
            asp_rules = self._convert_rule(head, body)
            self.rule_idx += 1

            # print('\n ASP Conversion')
            # for r in asp_rules:
            #     print(r)
            # print('\n')

            # TODO: Cleaner way to add/return rules?
            for r in asp_rules[:-1]:
                builder.add(r)

            return asp_rules[-1]

    def visit_Variable(self, variable: AST) -> AST:
        """
        Collects all global variables encountered in a rule
        """
        if variable not in self.global_variables:
            self.global_variables.append(variable)
        return variable

    def visit_TheoryAtom(self, atom: AST) -> AST:
        """
        Extracts the weight of the rule and removes the theory atom
        """
        self.weight = atom.term.arguments[0]
        # TODO: Better way to remove TheoryAtom?
        return ast.BooleanConstant(True)

    # def visit_Interval(self, interval: AST):
    #     """
    #     Collects any interval encountered in a rule
    #     """
    #     interval_variable = ast.Variable(
    #         interval.location, f'Interval{self.expansion_variables}')
    #     conversion = ast.Literal(
    #         interval.location, ast.Sign.NoSign,
    #         ast.Comparison(5, interval_variable, interval))
    #     self.global_variables.append(interval_variable)
    #     self.expansions_in_body.append(conversion)
    #     self.expansion_variables += 1
    #     return interval_variable

    # def visit_Pool(self, pool: AST):
    #     """
    #     Collects any pool encountered in a rule
    #     """
    #     # TODO: Check if pool is already bound to a variable
    #     # TODO: How to make sure variable is not used already?
    #     pool_variable = ast.Variable(pool.location,
    #                                  f'Pool{self.expansion_variables}')
    #     conversion = ast.Literal(pool.location, ast.Sign.NoSign,
    #                              ast.Comparison(5, pool_variable, pool))
    #     self.global_variables.append(pool_variable)
    #     self.expansions_in_body.append(conversion)
    #     self.expansion_variables += 1
    #     return pool_variable
