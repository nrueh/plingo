from typing import Sequence, cast
import sys

from clingo import clingo_main, Application, Control
from clingo import ApplicationOptions, Flag, Function
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
        self.query = []
        self.evidence_file = ''

    def _parse_query(self, value):
        """
        Parse query atom.
        """
        # TODO: What assertion does input query have to fulfill?
        self.query.append(value)
        return True

    def _parse_evidence(self, value):
        """
        Parse evidence.
        Has to be specified as clingo file
        """
        self.evidence_file = self._read(value)
        return True

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
        options.add(group, 'evid', 'Provide evidence file',
                    self._parse_evidence)

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

    def _ground_queries(self, symbolic_atoms):
        # TODO: Add warning if query not present in program?
        query_signatures = [
            s for s in symbolic_atoms.signatures if s[0] in self.query
        ]
        self.query = []
        for qs in query_signatures:
            for sa in symbolic_atoms.by_signature(qs[0], qs[1], qs[2]):
                self.query.append([sa.symbol, []])

    def _check_model_for_query(self, model):
        for qa in self.query:
            if model.contains(qa[0]):
                qa[1].append(model.number - 1)
        # for a in model.symbols(atoms=True):
        #     if a.name in self.query.keys():
        #         self.query[a.name].append([str(a), model.number - 1])

    def main(self, ctl: Control, files: Sequence[str]):
        '''
        Parse LP^MLN program and convert to ASP with weak constraints.
        '''
        ctl.add("base", [], THEORY)
        ctl.add("base", [], self.evidence_file)

        if self.display_all_probs:
            ctl.configuration.solve.opt_mode = 'enum,9999999999999'
            ctl.configuration.solve.models = 0

        if not files:
            files = ["-"]
        self._convert(ctl, files)

        ctl.ground([("base", [])])
        self._ground_queries(ctl.symbolic_atoms)

        # TODO: Handle optimum/all probability cases
        model_costs = []
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                if self.display_all_probs or self.query != []:
                    model_costs.append(model.cost)
                    if self.query != []:
                        self._check_model_for_query(model)

        if self.display_all_probs or self.query != []:
            probs = ProbabilityModule(model_costs, self.translate_hard_rules)
            if self.display_all_probs:
                probs.print_probs()
            if self.query != []:
                probs.get_query_probability(self.query)


if __name__ == '__main__':
    sys.exit(int(clingo_main(LPMLNApp(), sys.argv[1:])))
