from clingo import ast


def lit(func):
    return ast.Literal(func.location, 0, ast.SymbolicAtom(func))


class ConvertPlog:
    def _get_tuple(self, attr):
        loc = attr.location
        attr_name = ast.Function(loc, attr.name, [], False)
        domain_vars, range_var = attr.arguments[:-1], attr.arguments[-1]
        domain_tup = ast.Function(loc, '', domain_vars, False)
        return ast.Function(loc, '', [attr_name, domain_tup, range_var], False)

    def convert_random(self, ta, body):
        '''
        Input:
            &random(r1) { name(D, Y) : range(Y) } :- domain(D).
        Output:
            _random(r1, (name, D, Y)) :- range(Y), domain(D).
            _h((name, D, Y)) :- name(D, Y).
            name(D, Y) :- _h((name, D, Y)).
        '''
        loc = ta.location
        exp = ta.term.arguments[0]
        attr = ta.elements[0].terms[0]
        range = ta.elements[0].condition[0]

        attr_tup = self._get_tuple(attr)
        _random = ast.Function(loc, '_random', [exp, attr_tup], False)

        body.insert(0, range)
        _random_rule = ast.Rule(loc, lit(_random), body)

        hold = ast.Function(loc, '_h', [attr_tup], False)
        attr = ast.Function(loc, attr.name, [v for v in attr.arguments], False)
        readable_to_meta = ast.Rule(loc, lit(hold), [lit(attr)])
        meta_to_readable = ast.Rule(loc, lit(attr), [lit(hold)])
        return [_random_rule, readable_to_meta, meta_to_readable]

    def convert_pr(self, ta, body):
        '''
        Input:
            &pr(r1) { name(D, Y) } = "3/20"  :- body(D, Y).
        Output:
            _pr(r1, (name,D, Y), "3/20") :- body(D, Y).
        '''
        loc = ta.location
        exp = ta.term.arguments[0]
        attr = ta.elements[0].terms[0]
        prob = ta.guard.term

        attr_tup = self._get_tuple(attr)
        _pr = ast.Function(loc, '_pr', [exp, attr_tup, prob], False)

        _pr_rule = ast.Rule(loc, lit(_pr), body)
        return [_pr_rule]

    def convert_obs_do(self, ta):
        '''
        &obs { name(dom, val) } = bool. -> _obs((name, dom, val), bool).
            bool can be omitted and is true by default

        &do { name(dom, val) }.        -> _do((name, dom, val)).
        '''
        loc = ta.location
        attr = ta.elements[0].terms[0]
        attr_tup = self._get_tuple(attr)
        args = [attr_tup]
        if ta.term.name == 'obs':
            if ta.guard is not None:
                args.append(ta.guard.term)
            else:
                args.append(ast.Function(loc, 'true', [], False))
        _func = ast.Function(loc, f'_{ta.term.name}', args, False)
        return [ast.Rule(loc, lit(_func), [])]
