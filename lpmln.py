from typing import Any, List, Sequence, Mapping, Optional, MutableMapping, Set, cast
from copy import copy
import sys

from clingo import ast, Symbol, SymbolType, TheoryTerm, TheoryTermType, Number, String
from clingo import Flag, Function, Model, PropagateInit, PropagateControl, Assignment
from clingo import clingo_main, Application, Tuple_, Control, parse_program
from clingo import ProgramBuilder, Propagator, ApplicationOptions, SolveResult, parse_term
from clingo.ast import AST

from utils import Transformer


class LPMLNTransformer(Transformer):
    '''
    Transforms LP^MLN rules to ASP with weak constraints in the 'Penalty Way'
    '''
    def _get_parameters(self, rule: AST, weight):
        #TODO: Can rule be left out as argument? Needed for location?
        if weight == 'alpha':
            constraint_weight = Number(1)
            priority = Number(1)
        else:
            weight = Number(weight)
            constraint_weight = weight
            priority = Number(0)
        constraint_weight = ast.Symbol(rule.location, constraint_weight)
        priority = ast.Symbol(rule.location, priority)
        return weight, constraint_weight, priority

    def _get_unsat_atoms(self, rule: AST, weight, idx: int):
        idx = ast.Symbol(rule.location, Number(idx))
        weight = ast.Symbol(rule.location, weight)
        unsat_arguments = [idx, weight] + self.global_variables

        # TODO: Cleaner way to add variables?
        unsat = ast.SymbolicAtom(
            ast.Function(rule.location, "unsat", unsat_arguments, False))

        # unsat = ast.Function(rule.location, "unsat", [Number(idx), weight], False)
        not_unsat = ast.Literal(rule.location, ast.Sign.Negation, unsat)
        unsat = ast.Literal(rule.head.location, ast.Sign.NoSign, unsat)
        return unsat, not_unsat

    def _convert_rule(self, rule, weight, idx: int):
        self.global_variables = []
        weight, constraint_weight, priority = self._get_parameters(
            rule, weight)

        head = rule.head
        body = rule.body

        self.visit(head)
        self.visit(body)

        unsat, not_unsat = self._get_unsat_atoms(rule, weight, idx)

        # TODO: Fix that converter can handle aggregates
        if str(head.type) == 'Aggregate':
            not_head = ast.Literal(head.location, ast.Sign.NoSign,
                                   ast.BooleanConstant(True))
        # Fix that integrity constraints will be accepted by grounder.
        elif str(head.atom.type) == 'BooleanConstant' and not head.atom.value:
            not_head = ast.Literal(head.location, ast.Sign.NoSign,
                                   ast.BooleanConstant(True))
        else:
            not_head = ast.Literal(head.location, ast.Sign.Negation, head.atom)

        # Create ASP rules
        asp_rule1 = ast.Rule(rule.location, unsat, body + [not_head])
        asp_rule2 = ast.Rule(rule.location, head, body + [not_unsat])
        asp_rule3 = ast.Minimize(rule.location, constraint_weight, priority,
                                 [], [unsat])
        return asp_rule1, asp_rule2, asp_rule3

    def visit_Rule(self, rule: AST, weight, idx: int, builder: ProgramBuilder,
                   translate_hr: bool):
        """
        Visit rule, convert it to three ASP rules and
        add it to the program builder.
        """

        # print(head.elements[0].literal.child_keys)
        # print(head)
        # print(idx)
        # print(head.elements[0].literal.child_keys.atom)

        # TODO: Add visitor design pattern to extract variables
        # TODO: Setting that toggles whether hard rules are translated
        if weight == 'alpha' and not translate_hr:
            builder.add(rule)
        else:
            asp_rule1, asp_rule2, asp_rule3 = self._convert_rule(
                rule, weight, idx)
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


class LPMLNApp(Application):
    '''
    Application extending clingo with probabilistic logic language LP^MLN.
    '''
    program_name: str = "clingo-lpmln"
    version: str = "1.0"

    def __init__(self):
        self.translate_hard_rules = Flag(False)

    def _read(self, path: str):
        if path == "-":
            return sys.stdin.read()
        with open(path) as file_:
            return file_.read()

    def _extract_weight(self, lpmln_rule: str):
        # Extracts weight from (soft) rules
        # Weights are prepended and separated by '::'
        if '::' in lpmln_rule:
            split = lpmln_rule.split('::')
            weight = split[0].strip()
            if str(weight) != 'alpha':
                try:
                    weight = int(weight)
                except (ValueError):
                    raise AssertionError(
                        "Weight has to be 'alpha' or an integer")

            lpmln_rule = split[1].strip()

        # Hard rules have weight 'alpha' (can be omitted from encoding)
        else:
            weight = 'alpha'

        return lpmln_rule, weight

    def _parse_lpmln(self, ctl: Control, files: Sequence[str]):
        with ctl.builder() as b:
            lt = LPMLNTransformer()
            idx = 0
            for path in files:
                lines = self._read(path).splitlines()
                for lpmln_rule in lines:
                    lpmln_rule = lpmln_rule.strip()

                    # Skip comments and blank lines
                    if lpmln_rule == '' or lpmln_rule[0] == '%':
                        continue

                    lpmln_rule, weight = self._extract_weight(lpmln_rule)
                    parse_program(
                        lpmln_rule, lambda stm: lt.visit(
                            stm, weight, idx, b, self.translate_hard_rules))
                    idx += 1
            # ctl.cleanup()

    def _extract_atoms(self, model):
        atoms = model.symbols(atoms=True)
        show_atoms = []
        unsat_atoms = []
        for a in atoms:
            if a.name == 'unsat':
                unsat_atoms.append(a)
            else:
                show_atoms.append(a)
        return show_atoms, unsat_atoms

    def _on_model(self, model: Model):
        atoms = model.symbols(atoms=True)
        print(atoms)
        show_atoms = []
        unsat_atoms = []
        for a in atoms:
            if a.name == 'unsat':
                unsat_atoms.append(a)
                # print(a.arguments[1].number)
            else:
                show_atoms.append(a)
        # print(show_atoms)
        # TODO: Remove brackets when printing
        # print(show_atoms)
        # print(unsat_atoms)
        #print(','.join(str(show_atoms)))

    def register_options(self, options: ApplicationOptions) -> None:
        """
        Register application option.
        """
        group = 'LPMLN Options'
        options.add_flag(group, 'hr', 'Translate hard rules',
                         self.translate_hard_rules)

    def main(self, ctl: Control, files: Sequence[str]):
        '''
        Parse LP^MLN program and convert to ASP with weak constraints.
        '''
        if not files:
            files = ["-"]

        # ctl.configuration.solve.opt_mode = 'enum'
        # ctl.configuration.solve.models = 0

        self._parse_lpmln(ctl, files)
        ctl.add("base", [], "#show.")
        ctl.ground([("base", [])])
        # for sa in ctl.symbolic_atoms:
        #     print(sa.symbol)
        #     print(sa.literal)
        # ctl.solve(on_model=print)

        models_show = []
        models_unsat = []
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                show_atoms, unsat_atoms = self._extract_atoms(model)
                # print(show_atoms)
                # print(unsat_atoms)
                models_show.append(show_atoms)
                models_unsat.append(unsat_atoms)

        #print(models_show)
        # print(models_unsat)


def test(rule):
    if str(rule.type) == 'Minimize':
        print(rule.weight.type)


if __name__ == '__main__':
    # parse_program(':~ a. [1@3]', test)
    sys.exit(int(clingo_main(LPMLNApp(), sys.argv[1:])))
