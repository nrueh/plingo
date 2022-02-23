from typing import cast, Sequence
import sys

from clingo import clingo_main, Application, Control
from clingo import ApplicationOptions, Flag, Function, Number
from clingo.ast import AST, ProgramBuilder, parse_files
from clingo.configuration import Configuration
from clingo.script import enable_python

from transformer import PlingoTransformer
import query
from opt import MinObs, OptEnum
from probability import ProbabilityModule

THEORY = """
#theory plingo{
    constant { };
    &query/1: constant, head
}.
"""


class PlingoApp(Application):
    '''
    Application extending clingo with weighted rules
    and probability calculation module.
    Plingo can compute other probabilistic logic languages
    LP^MLN, ProbLog and P-Log.
    '''
    program_name: str = "plingo"
    version: str = "1.0"

    def __init__(self):
        self.translate_hard_rules = Flag(False)
        self.display_all_probs = Flag(False)
        self.use_unsat_approach = Flag(False)
        self.two_solve_calls = Flag(False)
        self.calculate_plog = Flag(False)
        self.use_backend = Flag(False)
        self.query = []
        self.evidence_file = ''
        self.balanced_models = None
        self.power_of_ten = 5

    def _parse_query(self, value):
        """
        Parse query atom specified through command-line.
        If query is passed with arguments (separated through comma),
        create a clingo.Function.
        Otherwise save the string of the atom name.
        """
        # TODO: What assertion does input query have to fulfill?
        if ',' in value:
            name = value.split(',')[0]
            args = []
            for a in value.split(',')[1:]:
                try:
                    args.append(Number(int(a)))
                except (ValueError):
                    args.append(Function(a))
            value = Function(name, args)
        self.query.append(value)
        return True

    def _parse_evidence(self, value):
        """
        Parse evidence.
        Has to be specified as (clingo) file path.
        """
        self.evidence_file = self._read(value)
        return True

    def _parse_balanced_query(self, value):
        """
        Sets number of models N to find for
        balanced query approximation.
        This will determine max. N models
        with and without the query.
        """
        # print(value)
        try:
            self.balanced_models = int(value)
            if self.balanced_models < 1:
                raise ValueError
            return True
        except ValueError:
            print(
                "Warning: --balanced N has to be set to an integer large than 0."
            )
            return False

    def register_options(self, options: ApplicationOptions) -> None:
        """
        Register application option.
        """
        group = 'Plingo Options'
        options.add_flag(group, 'hr', 'Translate hard rules',
                         self.translate_hard_rules)
        options.add_flag(group, 'all,a', 'Display all probabilities',
                         self.display_all_probs)
        options.add_flag(group, 'unsat', 'Convert using unsat atoms',
                         self.use_unsat_approach)
        options.add_flag(
            group, 'two-solve-calls',
            '''Use two solve calls (first determines LPMLN stable models, second their probabilities).
                            Works only with --hr options.''',
            self.two_solve_calls)
        options.add_flag(group, 'plog', 'Calculate P-Log program.',
                         self.calculate_plog)
        options.add(group,
                    'query',
                    'Probability of query atom',
                    self._parse_query,
                    multi=True)
        options.add(group, 'evid', 'Provide evidence file',
                    self._parse_evidence)
        options.add(
            group, 'balanced,b', '''Approximate query in a balanced way.
                            Use as --balanced N, where max. 2N models are determined
                            (N models with query true and false respectively).
                            This overwrites the --models option
                            This works only for a single (ground) query atom!''',
            self._parse_balanced_query)
        options.add_flag(
            group, 'use-backend',
            'Adds constaints for query approximation in backend instead of using assumptions.',
            self.use_backend)

    def validate_options(self):
        if self.two_solve_calls and not self.translate_hard_rules:
            print(
                'The two-solve-calls mode only works if hard rules are translated.'
            )
            return False
        return True

    def _read(self, path: str):
        if path == "-":
            return sys.stdin.read()
        with open(path) as file_:
            return file_.read()

    def _convert(self, ctl: Control, files: Sequence[str]):
        options = [
            self.translate_hard_rules, self.use_unsat_approach,
            self.two_solve_calls, self.power_of_ten
        ]
        with ProgramBuilder(ctl) as b:
            lt = PlingoTransformer(options)
            parse_files(files, lambda stm: b.add(cast(AST, lt.visit(stm, b))))

    def main(self, ctl: Control, files: Sequence[str]):
        '''
        Parse clingo program with weights and convert to ASP with weak constraints.
        '''

        ctl.add("base", [], THEORY)
        ctl.add("base", [], self.evidence_file)

        # Add meta file for calculating P-Log
        if self.calculate_plog:
            enable_python()
            ctl.add("base", [], self._read('examples/plog/meta.lp'))
            ctl.add("base", [], f'#const _plingo_factor={self.power_of_ten}.')
        if self.two_solve_calls:
            ctl.add("base", [], '#external _plingo_ext_helper.')
        # TODO: Make sure the _ext_helper atom is not contained in the program.
        # TODO: Change number of underscores for _ext_helper and plog meta atoms

        if not files:
            files = ["-"]
        self._convert(ctl, files)

        solve_config = cast(Configuration, ctl.configuration.solve)
        obs = MinObs(solve_config.opt_mode)
        ctl.register_observer(obs)

        ctl.ground([("base", [])])

        # Get theory queries in input program
        for t in ctl.theory_atoms:
            if t.term.name == 'query':
                self.query.append(query.convert_theory_query(t))
        if self.query != []:
            self.query = query.collect(self.query, ctl.symbolic_atoms)
            if self.balanced_models is not None and len(self.query) > 1:
                raise RuntimeError(
                    'Only one (ground) query atom can be specified for balanced approximation.'
                )

        # Solve
        if solve_config.opt_mode == 'optN':
            opt = OptEnum(self.query, self.balanced_models, self.use_backend)
            model_costs, self.query = opt._optimize(ctl, obs)
        else:
            bound_hr = 2**63 - 1
            if self.two_solve_calls:
                # First solve call
                # Soft rules are deactivated
                # TODO: Suppress output of first solve call, add flag
                # TODO: Activate this per flag

                ctl.assign_external(Function("_plingo_ext_helper"), False)
                with ctl.solve(yield_=True) as h:
                    for m in h:
                        bound_hr = m.cost[0]
                # TODO: Don't show _ext_helper
                ctl.assign_external(Function("_plingo_ext_helper"), True)

            if self.display_all_probs or self.query != []:
                ctl.configuration.solve.opt_mode = f'enum, {bound_hr}, {(2**63)-1}'
                ctl.configuration.solve.models = 0

            model_costs = []
            with ctl.solve(yield_=True) as handle:
                for model in handle:
                    if self.display_all_probs or self.query != []:
                        model_costs.append(model.cost)
                        if self.query != []:
                            self.query = query.check_model_for_query(
                                self.query, model)

        if model_costs != []:
            if 0 not in obs.priorities:
                # TODO: Should this be error or warning?
                print(
                    'No soft weights in program. Cannot calculate probabilites'
                )
            # TODO: What about case where there are other priorities than 0/1?
            # elif not self.two_solve_calls and any(
            #         x > 1 for x in obs.priorities):
            #     print(obs.priorities)
            #     print('testasd')
            else:
                probs = ProbabilityModule(model_costs, obs.priorities, [
                    self.translate_hard_rules, self.two_solve_calls,
                    self.power_of_ten
                ])
                if self.display_all_probs:
                    probs.print_probs()
                if self.query != []:
                    probs.get_query_probability(self.query)


if __name__ == '__main__':
    sys.exit(int(clingo_main(PlingoApp(), sys.argv[1:])))
