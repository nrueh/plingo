from clingo import ast, Number


def lit(func):
    return ast.Literal(func.location, 0, ast.SymbolicAtom(func))


class ConvertPlog:
    def __get_experiment_id(self, args):
        if len(args) != 0:
            if str(args[0].ast_type).endswith('Function'):
                exp_id = args[0].name
            elif str(args[0].ast_type).endswith('SymbolicTerm'):
                exp_id = args[0].symbol.name
        else:
            exp_id = ''
        return exp_id

    def __get_tuple(self, attr, exp_id=''):
        loc = attr.location
        attr_name = ast.Function(loc, attr.name, [], False)
        domain_vars, range_var = attr.arguments[:-1], attr.arguments[-1]
        domain_tup = ast.Function(loc, '', domain_vars, False)
        attr_tup = ast.Function(loc, '', [attr_name, domain_tup, range_var],
                                False)
        if exp_id == '':
            exp_args = [attr_name, domain_tup]
        else:
            exp_id = ast.Function(loc, exp_id, [], False)
            exp_args = [exp_id, attr_name, domain_tup]
        exp_tup = ast.Function(loc, '', exp_args, False)
        return exp_tup, attr_tup,

    def convert_random(self, ta, body):
        '''
        Input:
            &random(r1(D)) { name(D, Y) : range(Y) } :- domain(D).
                or
            &random(r1) { name(D, Y) : range(Y) } :- domain(D).
                or if one random rule per attribute
            &random { name(D, Y) : range(Y) } :- domain(D).
        Output:
            1. _random(r1, (name, D, Y)) :- range(Y), domain(D).
                  or
                _random((name,D), (name,D,Y)) :- range(Y), domain(D).
            2. _h((name, D, Y)) :- name(D, Y).
            3. { name(D, Y) : _random(_, (name, D, Y))} = 1 :-
                                            _random(_, (name, D, _)).
        '''
        loc = ta.location
        exp_id = self.__get_experiment_id(ta.term.arguments)

        attr = ta.elements[0].terms[0]
        range = ta.elements[0].condition[0]

        exp_tup, attr_tup = self.__get_tuple(attr, exp_id)
        _random = ast.Function(loc, '_random', [exp_tup, attr_tup], False)

        body.insert(0, range)
        _random_rule = ast.Rule(loc, lit(_random), body)

        hold = ast.Function(loc, '_h', [attr_tup], False)
        attr = ast.Function(loc, attr.name, [v for v in attr.arguments], False)
        readable_to_meta = ast.Rule(loc, lit(hold), [lit(attr)])

        anon = ast.Variable(loc, '_')
        _random_anon = _random.update(arguments=[anon, attr_tup])
        cond_lit = ast.ConditionalLiteral(loc, lit(attr), [lit(_random_anon)])
        guard = ast.AggregateGuard(5, ast.SymbolicTerm(loc, Number(1)))
        agg = ast.Aggregate(loc, None, [cond_lit], guard)
        attr_tup_anon = attr_tup.update(
            arguments=[attr_tup.arguments[0], attr_tup.arguments[1], anon])
        _random_anon2 = _random.update(arguments=[anon, attr_tup_anon])
        gen_rule = ast.Rule(loc, agg, [lit(_random_anon2)])
        return [_random_rule, readable_to_meta, gen_rule]

    def convert_pr(self, ta, body):
        '''
        Input:
            &pr(r1(D))  { name(D, Y) } = "3/20"  :- body(D, Y).
                or
            &pr(r1)     { name(D, Y) } = "3/20"  :- body(D, Y).
                or if one random rule per attribute
            &pr         { name(D, Y) } = "3/20"  :- body(D, Y).
        Output:
            _pr((r1, name, D), (name,D, Y), "3/20") :- body(D, Y).
                or
            _pr((name, D), (name,D, Y), "3/20") :- body(D, Y).
        '''
        loc = ta.location
        exp_id = self.__get_experiment_id(ta.term.arguments)

        attr = ta.elements[0].terms[0]
        prob = ta.guard.term

        exp_tup, attr_tup = self.__get_tuple(attr, exp_id)
        _pr = ast.Function(loc, '_pr', [exp_tup, attr_tup, prob], False)

        _pr_rule = ast.Rule(loc, lit(_pr), body)
        return [_pr_rule]

    def convert_obs(self, ta):
        '''
        &obs { name(D, Y) } = bool. -> _obs((name, D, Y), bool).
            bool can be omitted and is true by default
        '''
        loc = ta.location
        attr = ta.elements[0].terms[0]
        _, attr_tup = self.__get_tuple(attr)
        args = [attr_tup]

        if ta.guard is not None:
            args.append(ta.guard.term)
        else:
            args.append(ast.Function(loc, 'true', [], False))
        _obs = ast.Function(loc, f'_{ta.term.name}', args, False)
        return [ast.Rule(loc, lit(_obs), [])]

    def convert_do(self, ta):
        '''
        Input:
            &do { name(D, Y) }.
        Output:
            _do((name, D, Y)).
            name(D, Y) :- _do((name, D, Y)).
        '''
        loc = ta.location
        attr = ta.elements[0].terms[0]
        _, attr_tup = self.__get_tuple(attr)
        args = [attr_tup]
        _do = ast.Function(loc, f'_{ta.term.name}', args, False)

        attr = ast.Function(loc, attr.name, [v for v in attr.arguments], False)
        do_rule = ast.Rule(loc, lit(attr), [lit(_do)])
        return [ast.Rule(loc, lit(_do), []), do_rule]
