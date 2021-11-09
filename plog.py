from clingo import ast, Number


def lit(func):
    return ast.Literal(func.location, 0, ast.SymbolicAtom(func))


class ConvertPlog:
    def __get_tuple(self, attr):
        loc = attr.location
        attr_name = ast.Function(loc, attr.name, [], False)
        domain_vars, range_var = attr.arguments[:-1], attr.arguments[-1]
        domain_tup = ast.Function(loc, '', domain_vars, False)
        attr_tup = ast.Function(loc, '', [attr_name, domain_tup, range_var],
                                False)

        exp_tup = ast.Function(loc, attr.name, [domain_tup], False)
        return attr_tup, exp_tup

    def convert_random(self, ta, body):
        '''
        Input:
            &random(r(D)) { name(D,Y) : range(Y) } :- domain(D).
                or if one random rule per attribute
            &random       { name(D,Y) : range(Y) } :- domain(D).
        Output:
            Let E = r(D) or E = name(D)

            1. _random(E,(name,D,Y)) :- range(Y), domain(D).
            2. _h((name,D,Y)) :- name(D,Y).
            3. { name(D,Y) : _random(E,(name,D,Y))} = 1 :-
                                            _random(E,_).
        '''
        loc = ta.location
        attr = ta.elements[0].terms[0]
        range = ta.elements[0].condition[0]

        attr_tup, exp_tup = self.__get_tuple(attr)
        if len(ta.term.arguments) != 0:
            exp_tup = ta.term.arguments[0]

        _random = ast.Function(loc, '_random', [exp_tup, attr_tup], False)

        body.insert(0, range)
        _random_rule = ast.Rule(loc, lit(_random), body)

        hold = ast.Function(loc, '_h', [attr_tup], False)
        attr = ast.Function(loc, attr.name, [v for v in attr.arguments], False)
        readable_to_meta = ast.Rule(loc, lit(hold), [lit(attr)])

        # _random_anon = _random.update(arguments=[anon, attr_tup])
        cond_lit = ast.ConditionalLiteral(loc, lit(attr), [lit(_random)])
        guard = ast.AggregateGuard(5, ast.SymbolicTerm(loc, Number(1)))
        agg = ast.Aggregate(loc, None, [cond_lit], guard)
        # attr_tup_anon = attr_tup.update(
        #     arguments=[attr_tup.arguments[0], attr_tup.arguments[1], anon])
        anon = ast.Variable(loc, '_')
        _random_anon = _random.update(arguments=[exp_tup, anon])
        gen_rule = ast.Rule(loc, agg, [lit(_random_anon)])
        print(gen_rule)
        return [_random_rule, readable_to_meta, gen_rule]

    def convert_pr(self, ta, body):
        '''
        Input:
            &pr(r(D)) { name(D,Y) } = "3/20"  :- body(D,Y).
                or if one random rule per attribute
            &pr        { name(D,Y) } = "3/20"  :- body(D,Y).
        Output:
            Let E = r(D) or E = name(D)

            _pr(E,(name,D,Y),"3/20") :- body(D,Y).
        '''
        loc = ta.location
        attr = ta.elements[0].terms[0]
        prob = ta.guard.term

        attr_tup, exp_tup = self.__get_tuple(attr)
        if len(ta.term.arguments) != 0:
            exp_tup = ta.term.arguments[0]
        _pr = ast.Function(loc, '_pr', [exp_tup, attr_tup, prob], False)

        _pr_rule = ast.Rule(loc, lit(_pr), body)
        return [_pr_rule]

    def convert_obs(self, ta):
        '''
        &obs { name(D,Y) } = bool. -> _obs((name,D,Y), bool).
            bool can be omitted and is true by default
        '''
        loc = ta.location
        attr = ta.elements[0].terms[0]
        attr_tup, _ = self.__get_tuple(attr)
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
            &do { name(D,Y) }.
        Output:
            _do((name,D,Y)).
            name(D,Y) :- _do((name,D,Y)).
        '''
        loc = ta.location
        attr = ta.elements[0].terms[0]
        attr_tup, _ = self.__get_tuple(attr)
        args = [attr_tup]
        _do = ast.Function(loc, f'_{ta.term.name}', args, False)

        attr = ast.Function(loc, attr.name, [v for v in attr.arguments], False)
        do_rule = ast.Rule(loc, lit(attr), [lit(_do)])
        return [ast.Rule(loc, lit(_do), []), do_rule]
