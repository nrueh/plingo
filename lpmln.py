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
        self.query = []

    def _parse_query(self, value):
        """
        Parse query atom.
        """
        # TODO: What assertion does input query have to fulfill?
        self.query.append(value)
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
        # TODO: How input query? One flag per atom or define query as set of atom(s)?
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
        # TODO: Handle optimum/all probability cases
        models = []
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                models.append(
                    ([a for a in model.symbols(atoms=True)], model.cost))
                # print(model.cost)
                # show_atoms, unsat_atoms = self._extract_atoms(model)
                # print(show_atoms)
                # print(unsat_atoms)
                # models_show.append(show_atoms)
                # models_unsat.append(unsat_atoms)

        probs = ProbabilityModule(models, self.translate_hard_rules)

        if self.display_all_probs:
            probs.print_models_and_probs()

        if len(self.query) != 0:
            probs.get_query_probability(self.query)

        # print(models_show)
        # print(models_unsat)


if __name__ == '__main__':
    sys.exit(int(clingo_main(LPMLNApp(), sys.argv[1:])))
