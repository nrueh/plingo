from typing import Any, Sequence, cast
import sys

from clingo import ast, Number, String, Flag
from clingo import clingo_main, Application, Control
from clingo import ApplicationOptions
from clingo.ast import AST, ASTSequence, parse_string, ProgramBuilder

THEORY = """
#theory lpmln{
    constant { - : 0, unary };
    &weight/1 : constant, body
}.
"""


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
        idx, constraint_weight, priority = self._get_constraint_parameters(
            head.location)

        if str(head.ast_type) == 'ASTType.Aggregate':
            return [ast.Rule(head.location, head, body)]
            # not_head = ast.Literal(head.location, ast.Sign.Negation, head)
        else:
            not_head = ast.Literal(head.location, ast.Sign.Negation, head.atom)

        # Create ASP rules
        # TODO: Is it ok to use 'head.location' for the rules?
        # TODO: Better way to insert and delete items from body?

        if self.use_unsat:
            unsat, not_unsat = self._get_unsat_atoms(head.location, idx)
            # Rule 1 (unsat :- Body, not Head)
            body.insert(0, not_head)
            asp_rule1 = ast.Rule(head.location, unsat, body)

            # Rule 2 (Head :- Body, not unsat)
            del body[0]
            body.insert(0, not_unsat)
            asp_rule2 = ast.Rule(head.location, head, body)

            # Rule 3 (weak constraint unsat)
            asp_rule3 = ast.Minimize(head.location, constraint_weight,
                                     priority, [idx, self.global_variables],
                                     [unsat])
            return [asp_rule1, asp_rule2, asp_rule3]
        else:
            # Convert integrity constraint 'w: #false :- B.' to weak constraint
            # of form: ':~ B. [w, idx, X]'
            if str(head.atom.ast_type
                   ) == 'ASTType.BooleanConstant' and not head.atom.value:
                asp_rule = ast.Minimize(head.location, constraint_weight,
                                        priority, [idx, self.global_variables],
                                        body)
                return [asp_rule]
            # Convert normal rule 'w: H :- B.' to choice rule and weak
            # constraint of form: '{H} :- B.' and ':~ B, not H. [w, idx, X]'
            else:
                cond_head = ast.ConditionalLiteral(head.location, head, [])
                choice_head = ast.Aggregate(head.location, None, [cond_head],
                                            None)
                asp_rule1 = ast.Rule(head.location, choice_head, body)
                not_head = ast.Literal(head.location, ast.Sign.Negation,
                                       head.atom)
                body.insert(0, not_head)
                asp_rule2 = ast.Minimize(head.location, constraint_weight,
                                         priority,
                                         [idx, self.global_variables], body)
                return [asp_rule1, asp_rule2]

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


class LPMLNApp(Application):
    '''
    Application extending clingo with probabilistic logic language LP^MLN.
    '''
    program_name: str = "clingo-lpmln"
    version: str = "1.0"

    def __init__(self):
        self.translate_hard_rules = Flag(False)
        self.display_all_probs = Flag(False)
        self.use_unsat_approach = Flag(False)

    def _read(self, path: str):
        if path == "-":
            return sys.stdin.read()
        with open(path) as file_:
            return file_.read()

    def _convert(self, ctl: Control, files: Sequence[str]):
        options = [self.translate_hard_rules, self.use_unsat_approach]
        with ProgramBuilder(ctl) as b:
            lt = LPMLNTransformer(options)
            for path in files:
                parse_string(self._read(path),
                             lambda stm: b.add(cast(AST, lt.visit(stm, b))))

    def _extract_atoms(self, model):
        atoms = model.symbols(atoms=True)
        show_atoms = []
        unsat_atoms = []
        for a in atoms:
            if a.name == 'unsat':
                unsat_atoms.append(str(a))
            else:
                show_atoms.append(str(a))
        return show_atoms, unsat_atoms

    # def _on_model(self, model: Model):
    #     atoms = model.symbols(atoms=True)
    #     print(atoms)
    #     show_atoms = []
    #     unsat_atoms = []
    #     for a in atoms:
    #         if a.name == 'unsat':
    #             unsat_atoms.append(a)
    #             # print(a.arguments[1].number)
    #         else:
    #             show_atoms.append(a)
    #     # print(show_atoms)
    #     # TODO: Remove brackets when printing
    #     # print(show_atoms)
    #     # print(unsat_atoms)
    #     #print(','.join(str(show_atoms)))

    def register_options(self, options: ApplicationOptions) -> None:
        """
        Register application option.
        """
        group = 'LPMLN Options'
        options.add_flag(group, 'hr', 'Translate hard rules',
                         self.translate_hard_rules)
        options.add_flag(group, 'all', 'Display all probabilities',
                         self.display_all_probs)
        options.add_flag(group, 'unsat', 'Convert using unsat atoms',
                         self.use_unsat_approach)

    def main(self, ctl: Control, files: Sequence[str]):
        '''
        Parse LP^MLN program and convert to ASP with weak constraints.
        '''
        ctl.add("base", [], THEORY)
        ctl.add("base", [], "#show.")

        if self.display_all_probs:
            ctl.configuration.solve.opt_mode = 'enum,9999999999999'
            ctl.configuration.solve.models = 0

        if not files:
            files = ["-"]
        self._convert(ctl, files)

        ctl.ground([("base", [])])

        # ctl.solve(on_model=print)

        # models_show = []
        # models_unsat = []
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                show_atoms, unsat_atoms = self._extract_atoms(model)
                print(show_atoms)
                print(unsat_atoms)
                # models_show.append(show_atoms)
                # models_unsat.append(unsat_atoms)

        # print(models_show)
        # print(models_unsat)


if __name__ == '__main__':
    sys.exit(int(clingo_main(LPMLNApp(), sys.argv[1:])))
