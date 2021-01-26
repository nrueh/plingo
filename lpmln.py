from typing import Any, List, Sequence, Mapping, Optional, MutableMapping, Tuple, Set, cast
import sys

from clingo import ast, Symbol, SymbolType, TheoryTerm, TheoryTermType, Number
from clingo import Function, Model, PropagateInit, PropagateControl, Assignment
from clingo import clingo_main, Application, Tuple_, Control, parse_program
from clingo import Propagator, ApplicationOptions, SolveResult, parse_term
from clingo.ast import AST

THEORY = """
#theory lpmln{
    constant {
    -  : 0, unary
    };
    &weight/1 : constant, head
}.
"""


class WeightedRuleTransformer():
    def visit(self, rule: AST):
        print(rule.location)
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

    def _rewrite(self, ctl: Control, files: Sequence[str]):
        with ctl.builder() as b:
            wtr = WeightedRuleTransformer()
            for path in files:
                parse_program(
                    self._read(path),
                    lambda stm: b.add(cast(AST, wtr.visit(stm))))

    def main(self, ctl: Control, files: Sequence[str]):
        '''
        Register the difference constraint propagator, and then ground and
        solve.
        '''

        ctl.add("base", [], THEORY)

        if not files:
            files = ["-"]
  
        self._rewrite(ctl, files)

        ctl.ground([("base", [])])
        # ctl.solve(on_model=print)


if __name__ == '__main__':
    sys.exit(int(clingo_main(LPMLNApp(), sys.argv[1:])))
