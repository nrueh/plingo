from typing import Sequence, cast
import sys

from clingo import clingo_main, Application, Control
from clingo import ApplicationOptions, Flag, Function, Number
from clingo.ast import AST, ProgramBuilder, parse_files
from clingo.script import enable_python

from transformer import LPMLNTransformer
from probability import ProbabilityModule

THEORY = """
#theory lpmln{
    constant { };
    &query/1: constant, head
}.
"""
# TODO: Add evidence/1 to input language


class Observer:
    '''
    Observes levels of weak constraint priorities that have been added to
    the program to accurately calculate probabilities
    '''
    def __init__(self):
        self.priorities = []

    def minimize(self, priority: int, literals):
        self.priorities.append(priority)


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
        self.two_solve_calls = Flag(False)
        self.calculate_plog = Flag(False)
        self.query = []
        self.evidence_file = ''
        self.power_of_ten = 5

    def _parse_query(self, value):
        """
        Parse query atom.
        """
        # TODO: What assertion does input query have to fulfill?
        # TODO: Make it possible to specify queries with arguments
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
        options.add_flag(
            group, 'two-solve-calls',
            'Use two solve calls (first determines LPMLN stable models, \
                second their probabilities). \
                Works only with --hr options.', self.two_solve_calls)
        options.add_flag(group, 'plog', 'Calculate P-Log program.',
                         self.calculate_plog)
        options.add(group,
                    'q',
                    'Get probability of query atom',
                    self._parse_query,
                    multi=True)
        options.add(group, 'evid', 'Provide evidence file',
                    self._parse_evidence)

    # # TODO: Shows error: TypeError: an integer is required
    # def validate_options(self):
    #     if self.two_solve_calls and not self.translate_hard_rules:
    #         # TODO: Add error message
    #         return False

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
            lt = LPMLNTransformer(options)
            parse_files(files, lambda stm: b.add(cast(AST, lt.visit(stm, b))))
        # for q in lt.query:
        #     self.query.append(q)

    def _convert_theory_arg(self, arg):
        theory_type = str(arg.type)[15:]
        if theory_type == 'Symbol':
            return Function(arg.name)
        elif theory_type == 'Number':
            return Number(arg.number)
        elif theory_type == 'Function':
            args = [self._convert_theory_arg(targ) for targ in arg.arguments]
            return Function(arg.name, args)

    def _add_theory_query(self, theory_atom):
        query_atom = theory_atom.term.arguments[0]
        name = query_atom.name
        args = []
        if query_atom.arguments != []:
            args = [
                self._convert_theory_arg(arg) for arg in query_atom.arguments
            ]
        self.query.append(Function(name, args))

    def _ground_queries(self, symbolic_atoms):
        # TODO: Add warning if query not present in program?
        general_queries = []
        queries_with_args = []
        for q in self.query:
            if type(q) is str:
                general_queries.append(q)
            else:
                queries_with_args.append([q, []])

        query_signatures = [
            s for s in symbolic_atoms.signatures if s[0] in general_queries
        ]
        self.query = queries_with_args
        for qs in query_signatures:
            for sa in symbolic_atoms.by_signature(qs[0], qs[1], qs[2]):
                self.query.append([sa.symbol, []])

    def _check_model_for_query(self, model):
        for qa in self.query:
            if model.contains(qa[0]):
                qa[1].append(model.number - 1)

    def main(self, ctl: Control, files: Sequence[str]):
        '''
        Parse LP^MLN program and convert to ASP with weak constraints.
        '''
        observer = Observer()
        ctl.register_observer(observer)

        ctl.add("base", [], THEORY)
        ctl.add("base", [], self.evidence_file)
        if self.calculate_plog:
            enable_python()
            ctl.add("base", [], self._read('examples/plog/meta.lp'))
            ctl.add("base", [], f'#const _lpmln_factor={self.power_of_ten}.')
        if self.two_solve_calls:
            ctl.add("base", [], '#external _lpmln_ext_helper.')
        # TODO: Make sure the _ext_helper atom is not contained in the program.
        # TODO: Change number of underscores for _ext_helper and plog meta atoms

        if not files:
            files = ["-"]
        self._convert(ctl, files)

        ctl.ground([("base", [])])

        for t in ctl.theory_atoms:
            if t.term.name == 'query':
                self._add_theory_query(t)

        if self.query != []:
            self._ground_queries(ctl.symbolic_atoms)

        bound_hr = 2**63 - 1
        if self.two_solve_calls:
            # First solve call
            # Soft rules are deactivated
            # TODO: Suppress output of first solve call, add flag
            # TODO: Activate this per flag

            ctl.assign_external(Function("_lpmln_ext_helper"), False)
            with ctl.solve(yield_=True) as h:
                for m in h:
                    bound_hr = m.cost[0]
            # TODO: Don't show _ext_helper
            # ctl.release_external(Function("_ext_helper"))
            ctl.assign_external(Function("_lpmln_ext_helper"), True)

        if self.display_all_probs or self.query != []:
            ctl.configuration.solve.opt_mode = f'enum, {bound_hr}, {(2**63)-1}'
            ctl.configuration.solve.models = 0

        model_costs = []
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                if self.display_all_probs or self.query != []:
                    model_costs.append(model.cost)
                    if self.query != []:
                        self._check_model_for_query(model)

        if model_costs != [] and (self.display_all_probs or self.query != []):
            if 0 not in observer.priorities:
                # TODO: Should this be error or warning?
                print(
                    'No soft weights in program. Cannot calculate probabilites'
                )
            # TODO: What about case where there are other priorities than 0/1?
            # elif not self.two_solve_calls and any(
            #         x > 1 for x in observer.priorities):
            #     print(observer.priorities)
            #     print('testasd')
            else:
                probs = ProbabilityModule(model_costs, observer.priorities, [
                    self.translate_hard_rules, self.two_solve_calls,
                    self.power_of_ten
                ])
                if self.display_all_probs:
                    probs.print_probs()
                if self.query != []:
                    probs.get_query_probability(self.query)


if __name__ == '__main__':
    sys.exit(int(clingo_main(LPMLNApp(), sys.argv[1:])))
