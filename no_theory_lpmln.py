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
    def visit_Rule(self, rule: AST, weight, idx: int):
        head = rule.head
        body = rule.body
        print('\n LP^MLN Rule')
        print(rule)

        if weight == 'alpha':
            constraint_weight = 1
            priority = 1
        else:
            constraint_weight = weight
            weight = Number(weight)
            priority = 0

        unsat = Function("unsat", [Number(idx), weight])
        not_unsat = ast.Literal(rule.location, ast.Sign.Negation, unsat)

        asp_rule1 = ast.Rule(
            rule.location,
            unsat,
            body + [ast.Literal(head.location, ast.Sign.Negation, head)])
        asp_rule2 = ast.Rule(rule.location, head, body + [not_unsat])
        asp_rule3 = ast.Minimize(rule.location, constraint_weight, priority, [], [unsat])

        print('\n ASP Conversion')
        print(asp_rule1)
        print(asp_rule2)
        print(asp_rule3)
        return rule


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
                except(ValueError):
                    raise AssertionError("Weight has to be 'alpha' or an integer")

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
                    parse_program(
                        lpmln_rule,
                        lambda stm: b.add(cast(AST, lt.visit(stm, weight, i))))

    def main(self, ctl: Control, files: Sequence[str]):
        '''
        Parse LP^MLN program and convert to ASP with weak constraints.
        '''
        if not files:
            files = ["-"]

        self._parse_lpmln(ctl, files)

        ctl.ground([("base", [])])
        ctl.solve(on_model=print)

def test(rule):
    if str(rule.type) == 'Minimize':
        print(rule.weight.type)

if __name__ == '__main__':
    # parse_program(':~ a. [1@3]', test)
    sys.exit(int(clingo_main(LPMLNApp(), sys.argv[1:])))
