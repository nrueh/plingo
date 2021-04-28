from typing import Sequence, cast
import sys

from clingo import clingo_main, Application, Control
from clingo import ApplicationOptions, Flag
from clingo.ast import AST, parse_string, ProgramBuilder

from transformer import LPMLNTransformer
from probability import ProbabilityModule

THEORY = """
#theory lpmln{
    constant { - : 0, unary };
    &weight/1 : constant, body
}.
"""


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
        self.query = {}

    def _parse_query(self, value):
        """
        Parse query atom.
        """
        # TODO: What assertion does input query have to fulfill?

        # name = value.split(',')[0]
        # if ',' in value:
        #     arg = value.split(',')[1:]
        #     arg = [
        #         SymbolicTerm({
        #             'begin': '',
        #             'end': ''
        #         }, String(a)) for a in arg
        #     ]
        # else:
        #     arg = []
        # query_atom = Function(name, arg, True)
        self.query[value] = []
        return True

    def _check_model_for_query(self, model):
        # TODO: Use model.contains()?
        # for qa in self.query:
        #     print(qa)
        #     if model.contains(qa):
        #         print(str(qa))
        #         print("model contains query")
        for a in model.symbols(atoms=True):
            if a.name in self.query.keys():
                self.query[a.name].append([str(a), model.number - 1])

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
        options.add(group,
                    'q',
                    'Get probability of query atom',
                    self._parse_query,
                    multi=True)

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

    def main(self, ctl: Control, files: Sequence[str]):
        '''
        Parse LP^MLN program and convert to ASP with weak constraints.
        '''
        ctl.add("base", [], THEORY)

        if self.display_all_probs:
            ctl.configuration.solve.opt_mode = 'enum,9999999999999'
            ctl.configuration.solve.models = 0

        if not files:
            files = ["-"]
        self._convert(ctl, files)

        ctl.ground([("base", [])])

        # TODO: Handle optimum/all probability cases
        model_costs = []
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                model_costs.append(model.cost)
                if self.query != {}:
                    self._check_model_for_query(model)

        probs = ProbabilityModule(model_costs, self.translate_hard_rules)
        if self.display_all_probs:
            probs.print_probs()

        if self.query != {}:
            probs.get_query_probability(self.query)


if __name__ == '__main__':
    sys.exit(int(clingo_main(LPMLNApp(), sys.argv[1:])))
