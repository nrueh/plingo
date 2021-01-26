from typing import Any, List, Sequence, Mapping, Optional, MutableMapping, Tuple, Set, cast
import sys

from clingo import ast, Symbol, SymbolType, TheoryTerm, TheoryTermType, Number
from clingo import Function, Model, PropagateInit, PropagateControl, Assignment
from clingo import clingo_main, Application, Tuple_, Control, parse_program
from clingo import Propagator, ApplicationOptions, SolveResult, parse_term
from clingo.ast import AST

from utils import Transformer


class LPMLNTransformer(Transformer):
    def visit_Rule(self, rule: AST, weight: int):
        print(rule.head)
        print(rule.body)
        print(weight)
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
                for lpmln_rule in lines:
                    lpmln_rule = lpmln_rule.strip()

                    # Skip comments
                    if lpmln_rule[0] == '%':
                        continue

                    lpmln_rule, weight = self._extract_weight(lpmln_rule)
                    parse_program(
                        lpmln_rule,
                        lambda stm: b.add(cast(AST, lt.visit(stm, weight))))

    def main(self, ctl: Control, files: Sequence[str]):
        '''
        Parse LP^MLN program and convert to ASP with weak constraints.
        '''
        if not files:
            files = ["-"]

        self._parse_lpmln(ctl, files)

        ctl.ground([("base", [])])
        ctl.solve(on_model=print)


if __name__ == '__main__':
    sys.exit(int(clingo_main(LPMLNApp(), sys.argv[1:])))
