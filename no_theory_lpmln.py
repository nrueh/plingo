from typing import Any, List, Sequence, Mapping, Optional, MutableMapping, Tuple, Set, cast
from copy import copy
import sys

from clingo import ast, Symbol, SymbolType, TheoryTerm, TheoryTermType, Number
from clingo import Function, Model, PropagateInit, PropagateControl, Assignment
from clingo import clingo_main, Application, Tuple_, Control, parse_program
from clingo import Propagator, ApplicationOptions, SolveResult, parse_term
from clingo.ast import AST

from utils import Transformer


class LPMLNTransformer(Transformer):
    '''
    Transforms LP^MLN rules to ASP with weak constraints in the 'Penalty Way'
    '''
    def _get_parameters(self, rule: AST, weight):
        #TODO: Can you leave out rule as argument? Needed for location?
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
        unsat = ast.SymbolicAtom(
            ast.Symbol(rule.location, Function("unsat",
                                               [Number(idx), weight])))
        # unsat = ast.Function(rule.location, "unsat", [Number(idx), weight], False)
        not_unsat = ast.Literal(rule.location, ast.Sign.Negation, unsat)
        unsat = ast.Literal(rule.head.location, ast.Sign.NoSign, unsat)
        return unsat, not_unsat

    def visit_Rule(self, rule: AST, weight, idx: int, builder):
        """
        Visit rule, convert it to three ASP rules and
        add it to the program builder.
        """
        head = rule.head
        body = rule.body
        # print('\n LP^MLN Rule')
        # print(rule)

        weight, constraint_weight, priority = self._get_parameters(
            rule, weight)
        unsat, not_unsat = self._get_unsat_atoms(rule, weight, idx)

        not_head = ast.Literal(head.location, ast.Sign.Negation, head.atom)

        asp_rule1 = ast.Rule(rule.location, unsat, body + [not_head])
        asp_rule2 = ast.Rule(rule.location, head, body + [not_unsat])
        asp_rule3 = ast.Minimize(rule.location, constraint_weight, priority,
                                 [], [unsat])

        # print('\n ASP Conversion')
        # print(asp_rule1)
        # print(asp_rule2)
        # print(asp_rule3)
        builder.add(asp_rule1)
        builder.add(asp_rule2)
        builder.add(asp_rule3)
        # return asp_rule3


class LPMLNApp(Application):
    '''
    Application extending clingo with probabilistic logic language LP^MLN.
    '''
    program_name: str = "clingo-lpmln"
    version: str = "1.0"

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
            weight = split[0]
            if weight != 'alpha':
                try:
                    weight = int(weight)
                except (ValueError):
                    raise AssertionError(
                        "Weight has to be 'alpha' or an integer")

            lpmln_rule = split[1].strip()

        # Hard rules have weight 'alpha' (can be omitted from code)
        else:
            weight = 'alpha'

        return lpmln_rule, weight

    def _parse_lpmln(self, ctl: Control, files: Sequence[str]):
        with ctl.builder() as b:
            lt = LPMLNTransformer()
            for path in files:
                lines = self._read(path).splitlines()
                for i, lpmln_rule in enumerate(lines):
                    lpmln_rule = lpmln_rule.strip()

                    # Skip comments
                    if lpmln_rule[0] == '%':
                        continue

                    lpmln_rule, weight = self._extract_weight(lpmln_rule)
                    parse_program(lpmln_rule,
                                  lambda stm: lt.visit(stm, weight, i, b))

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

    def main(self, ctl: Control, files: Sequence[str]):
        '''
        Parse LP^MLN program and convert to ASP with weak constraints.
        '''
        if not files:
            files = ["-"]
        ctl.configuration.solve.models = 0
        ctl.configuration.solve.opt_mode = 'ignore'

        self._parse_lpmln(ctl, files)
        ctl.add("base", [], "#show.")
        ctl.ground([("base", [])])
        # ctl.solve(on_model=self._on_model)

        models_show = []
        models_unsat = []
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                show_atoms, unsat_atoms = self._extract_atoms(model)
                models_show.append(show_atoms)
                models_unsat.append(unsat_atoms)

        print(models_show)
        print(models_unsat)


def test(rule):
    if str(rule.type) == 'Minimize':
        print(rule.weight.type)


if __name__ == '__main__':
    # parse_program(':~ a. [1@3]', test)
    sys.exit(int(clingo_main(LPMLNApp(), sys.argv[1:])))
