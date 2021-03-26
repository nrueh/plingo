from typing import Any, Sequence
import sys

from clingo import ast, Number, String, Flag, Model
from clingo import clingo_main, Application, Control
from clingo import ApplicationOptions
from clingo.ast import AST, ASTSequence, parse_string, ProgramBuilder, Transformer

# from utils import Transformer

THEORY = """
#theory lpmln{
    constant { - : 0, unary };
    &weight/1 : constant, body
}.
"""


class LPMLNTransformer(Transformer):
    '''
    Transforms LP^MLN rules to ASP with weak constraints in the 'Penalty Way'
    '''
    def __init__(self):
        self.rule_idx = 0

    def visit(self, ast: AST, *args: Any, **kwargs: Any) -> AST:
        '''
        Dispatch to a visit method in a base class or visit and transform the
        children of the given AST if it is missing.
        '''
        # TODO: Is this necessary?
        if isinstance(ast, AST):
            attr = 'visit_' + str(ast.ast_type).replace('ASTType.', '')
            if hasattr(self, attr):
                return getattr(self, attr)(ast, *args, **kwargs)
        if isinstance(ast, ASTSequence):
            return self.visit_sequence(ast, *args, **kwargs)
        return ast.update(**self.visit_children(ast, *args, **kwargs))

    def _get_constraint_parameters(self, location: dict):
        if self.weight == 'alpha':
            self.weight = ast.SymbolicTerm(location, String('alpha'))
            constraint_weight = ast.SymbolicTerm(location, Number(1))
            priority = Number(1)
        else:
            constraint_weight = self.weight
            priority = Number(0)
        priority = ast.SymbolicTerm(location, priority)
        return constraint_weight, priority

    def _get_unsat_atoms(self, location: dict):
        idx = ast.SymbolicTerm(location, Number(self.rule_idx))
        unsat_arguments = [idx, self.weight] + self.global_variables

        unsat = ast.SymbolicAtom(
            ast.Function(location, "unsat", unsat_arguments, False))

        # unsat = ast.Function(rule.location, "unsat", [Number(idx), weight], False)
        not_unsat = ast.Literal(location, ast.Sign.Negation, unsat)
        unsat = ast.Literal(location, ast.Sign.NoSign, unsat)

        return unsat, not_unsat

    def _convert_rule(self, head, body):
        constraint_weight, priority = self._get_constraint_parameters(
            head.location)
        unsat, not_unsat = self._get_unsat_atoms(head.location)

        # TODO: Fix that converter can handle aggregates
        if str(head.ast_type) == 'Aggregate':
            not_head = ast.Literal(head.location, ast.Sign.NoSign,
                                   ast.BooleanConstant(True))
        # Fix that integrity constraints will be accepted by grounder.
        # TODO: Better way for this?
        elif str(head.atom.ast_type
                 ) == 'ASTType.BooleanConstant' and not head.atom.value:
            not_head = ast.Literal(head.location, ast.Sign.NoSign,
                                   ast.BooleanConstant(True))
        else:
            not_head = ast.Literal(head.location, ast.Sign.Negation, head.atom)

        # Create ASP rules
        # TODO: Is it ok to use 'head.location' for the rules?
        # TODO: Better way to insert and delete items from body?

        # Rule 1 (unsat :- Body, not Head)
        body.insert(0, not_head)
        asp_rule1 = ast.Rule(head.location, unsat, body)

        #Rule 2 (Head :- Body, not unsat)
        del body[0]
        body.insert(0, not_unsat)
        asp_rule2 = ast.Rule(head.location, head, body)

        # Rule 3 (weak constraint unsat)
        asp_rule3 = ast.Minimize(head.location, constraint_weight, priority,
                                 [], [unsat])
        return asp_rule1, asp_rule2, asp_rule3

    def visit_Rule(self, rule: AST, builder: ProgramBuilder,
                   translate_hr: bool):
        """
        Visit rule, convert it to three ASP rules and
        add it to the program builder.
        """
        # Set weight to alpha by default
        self.weight = 'alpha'
        self.global_variables = []

        head = rule.head
        body = rule.body

        head = self.visit(head)
        body = self.visit(body)

        # print(repr(body))
        # print(self.global_variables)
        # print(self.weight)

        if self.weight == 'alpha' and not translate_hr:
            self.rule_idx += 1
            builder.add(ast.Rule(rule.location, head, body))
        else:
            asp_rule1, asp_rule2, asp_rule3 = self._convert_rule(head, body)
            self.rule_idx += 1
            # print('\n LP^MLN Rule')
            # print(rule)
            # print('\n ASP Conversion')
            # print(asp_rule1)
            # print(asp_rule2)
            # print(asp_rule3)

            builder.add(asp_rule1)
            builder.add(asp_rule2)
            builder.add(asp_rule3)

    def visit_Variable(self, variable: AST):
        if variable not in self.global_variables:
            self.global_variables.append(variable)
        return variable

    def visit_TheoryAtom(self, atom: AST):
        # print(atom.term.arguments[0])
        self.weight = atom.term.arguments[0]  #.symbol.number
        # TODO: Better way to remove TheoryAtom?
        return ast.BooleanConstant(True)


class LPMLNApp(Application):
    '''
    Application extending clingo with probabilistic logic language LP^MLN.
    '''
    program_name: str = "clingo-lpmln"
    version: str = "1.0"

    def __init__(self):
        self.translate_hard_rules = Flag(False)
        self.display_all_probs = Flag(False)

    def _read(self, path: str):
        if path == "-":
            return sys.stdin.read()
        with open(path) as file_:
            return file_.read()

    def _convert(self, ctl: Control, files: Sequence[str]):
        with ProgramBuilder(ctl) as b:
            lt = LPMLNTransformer()
            for path in files:
                parse_string(
                    self._read(path),
                    lambda stm: lt.visit(stm, b, self.translate_hard_rules))

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

    def main(self, ctl: Control, files: Sequence[str]):
        '''
        Parse LP^MLN program and convert to ASP with weak constraints.
        '''
        ctl.add("base", [], THEORY)
        # ctl.add("base", [], "#show.")

        if self.display_all_probs:
            ctl.configuration.solve.opt_mode = 'enum'
            ctl.configuration.solve.models = 0

        if not files:
            files = ["-"]
        self._convert(ctl, files)

        ctl.ground([("base", [])])

        ctl.solve(on_model=print)

        # models_show = []
        # models_unsat = []
        # with ctl.solve(yield_=True) as handle:
        #     for model in handle:
        #         show_atoms, unsat_atoms = self._extract_atoms(model)
        #         print(show_atoms)
        #         print(unsat_atoms)
        #         models_show.append(show_atoms)
        #         models_unsat.append(unsat_atoms)

        # print(models_show)
        # print(models_unsat)


if __name__ == '__main__':
    sys.exit(int(clingo_main(LPMLNApp(), sys.argv[1:])))
