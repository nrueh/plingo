from typing import cast, Sequence, Dict, List, Tuple, Optional
import sys

from clingo import clingo_main, Application, Control
from clingo import ApplicationOptions, Flag, Function, Number
from clingo.ast import AST, ProgramBuilder, parse_files
from clingo.backend import Backend, Observer
from clingo.configuration import Configuration
from clingo.script import enable_python
from clingo.solving import SolveResult, Model
from clingo.statistics import StatisticsMap

from transformer import PlingoTransformer
from probability import ProbabilityModule

THEORY = """
#theory plingo{
    constant { };
    &query/1: constant, head
}.
"""
# TODO: Add evidence/1 to input language


class MinObs(Observer):
    '''
    Observer to extract ground minimize constraint.
    '''
    literals: Dict[int, List[Tuple[int, int]]]

    def __init__(self):
        self.literals = {}

    def minimize(self, priority: int, literals: Sequence[Tuple[int, int]]):
        '''
        Intercept minimize constraint and add it to member `literals`.
        '''
        self.literals.setdefault(priority, []).extend(literals)


class PriorityObs(Observer):
    '''
    Observes levels of weak constraint priorities that have been added to
    the program to accurately calculate probabilities
    '''

    def __init__(self):
        self.priorities = []

    def minimize(self, priority: int, literals):
        self.priorities.append(priority)


class PlingoApp(Application):
    '''
    Application extending clingo with probabilistic logic language LP^MLN.
    '''
    program_name: str = "plingo"
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

        self._aux_level = {}
        self._proven = 0
        self._intermediate = 0

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
        group = 'Plingo Options'
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
            lt = PlingoTransformer(options)
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

    def _on_model(self, model: Model) -> bool:
        '''
        Intercept models.
        This function counts optimal and intermediate models as well as passes
        model to the restore heuristic.
        '''
        # if self._heu:
        #     self._heu.on_model(model)
        if model.optimality_proven:
            self.model_costs.append(model.cost)
            self._proven += 1
        else:
            self._intermediate += 1
        return True

    def _add_upper_bound(self, backend: Backend, wlits: Sequence[Tuple[int,
                                                                       int]],
                         bound: int, level: Optional[int]):
        '''
        Adds the constraint `a <> { wlits } < bound` and returns literal `a`.
        If level is None, then an integrity constraint is added and no
        auxiliary literal is introduced.
        This function reuses literals introduced in earlier iterations.
        '''
        hd = []
        if level is not None:
            if (level, bound) in self._aux_level:
                return self._aux_level[(level, bound)]
            hd.append(backend.add_atom())
            self._aux_level[(level, bound)] = hd[0]

        lower = -bound
        wlits_lower = []
        for l, w in wlits:
            if w > 0:
                lower += w
                l = -l
            else:
                w = -w
            wlits_lower.append((l, w))

        backend.add_weight_rule(hd, lower, wlits_lower)
        return hd[0] if hd else None

    def _set_upper_bound(self, backend: Backend,
                         minimize: Sequence[Sequence[Tuple[int, int]]],
                         bound: Sequence[int]):
        '''
        Adds constraints discarding solutions lexicographically smaller or
        equal than the bound.
        The weighted literals in the minimize variable directly correspond to
        how the solver represents minimize constraints.
        '''
        assert minimize and len(minimize) == len(bound)
        if len(minimize) == 1:
            self._add_upper_bound(backend, minimize[0], bound[0], None)
        else:
            # Note: we could also introduce a chain. But then there are
            # typically few priorities and this should resolve nicely.
            # :- l0 <= b0-1
            # :- l0 <= b0 && l1 <= b1-1
            # :- l0 <= b0 && l1 <= b1 && l2 <= b2-1
            # ...
            # :- l0 <= b0 && l1 <= b1 && l2 <= b2 && ... && ln <= bn
            prefix = []
            for i, (wlits, value) in enumerate(zip(minimize, bound)):
                if i == len(minimize) - 1:
                    prefix.append(
                        self._add_upper_bound(backend, wlits, value, i))
                    backend.add_rule([], prefix)
                else:
                    prefix.append(
                        self._add_upper_bound(backend, wlits, value - 1, i))
                    backend.add_rule([], prefix)
                    prefix[-1] = self._add_upper_bound(backend, wlits, value,
                                                       i)

    def _on_statistics(self, step: StatisticsMap, accu: StatisticsMap):
        '''
        Sets optimization specific statistics.
        '''
        #pylint: disable=unused-argument
        accu.update({
            'Enumerate': {
                'Enumerated': self._proven,
                'Intermediate': self._intermediate
            }
        })

    def _optimize(self, control: Control):
        '''
        Run optimal solution enumeration algorithm.
        '''
        obs = MinObs()
        control.register_observer(obs)

        # if self._restore:
        #     self._heu = RestoreHeu()
        #     control.register_propagator(self._heu)

        control.ground([('base', [])])
        res = cast(
            SolveResult,
            control.solve(on_model=self._on_model,
                          on_statistics=self._on_statistics))

        solve_config = cast(Configuration, control.configuration.solve)

        num_models = int(cast(str, solve_config.models))

        minimize = [
            x[1] for x in sorted(obs.literals.items(), key=lambda x: -x[0])
        ]

        while (res.satisfiable and not res.interrupted and minimize
               and 'costs' in control.statistics['summary']):
            summary = control.statistics['summary']
            if num_models > 0:
                num_models -= int(summary['models']['optimal'])
                if num_models <= 0:
                    break
                solve_config.models = num_models

            costs = cast(
                Tuple[int],
                tuple(int(x) for x in control.statistics['summary']['costs']))
            with control.backend() as backend:
                self._set_upper_bound(backend, minimize, costs)

            # if self._heu is not None:
            #     self._heu.set_restore(costs)

            res = cast(
                SolveResult,
                control.solve(on_model=self._on_model,
                              on_statistics=self._on_statistics))

    def main(self, ctl: Control, files: Sequence[str]):
        '''
        Parse LP^MLN program and convert to ASP with weak constraints.
        '''
        prio_obs = PriorityObs()
        ctl.register_observer(prio_obs)

        ctl.add("base", [], THEORY)
        ctl.add("base", [], self.evidence_file)
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

        bound_hr = 2**63 - 1
        self.model_costs = []
        if solve_config.opt_mode == 'optN':
            self._optimize(ctl)
        else:
            ctl.ground([("base", [])])

            for t in ctl.theory_atoms:
                if t.term.name == 'query':
                    self._add_theory_query(t)

            if self.query != []:
                self._ground_queries(ctl.symbolic_atoms)

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
                # ctl.release_external(Function("_ext_helper"))
                ctl.assign_external(Function("_plingo_ext_helper"), True)

            if self.display_all_probs or self.query != []:
                ctl.configuration.solve.opt_mode = f'enum, {bound_hr}, {(2**63)-1}'
                ctl.configuration.solve.models = 0

            with ctl.solve(yield_=True) as handle:
                for model in handle:
                    if self.display_all_probs or self.query != []:
                        self.model_costs.append(model.cost)
                        if self.query != []:
                            self._check_model_for_query(model)

        print(self.model_costs)
        if self.model_costs != []:
            if 0 not in prio_obs.priorities:
                # TODO: Should this be error or warning?
                print(
                    'No soft weights in program. Cannot calculate probabilites'
                )
            # TODO: What about case where there are other priorities than 0/1?
            # elif not self.two_solve_calls and any(
            #         x > 1 for x in prio_obs.priori´ties):
            #     print(prio_obs.priorities)
            #     print('testasd')
            else:
                probs = ProbabilityModule(
                    self.model_costs, prio_obs.priorities, [
                        self.translate_hard_rules, self.two_solve_calls,
                        self.power_of_ten
                    ])
                if self.display_all_probs:
                    probs.print_probs()
                if self.query != []:
                    probs.get_query_probability(self.query)


if __name__ == '__main__':
    sys.exit(int(clingo_main(PlingoApp(), sys.argv[1:])))
