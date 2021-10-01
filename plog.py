# from math import log

from clingo import ast

from utils import lit


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
            &random{ r1; name(D, Y) : range(Y) } :- domain(D).
        Output:
            _random(r1, (name, D, Y)) :- range(Y), domain(D).
            _h((name, D, Y)) :- name(D, Y).
            name(D, Y) :- _h((name, D, Y)).
            #show name/X. (X: arity of name(D, Y) atom)
        '''
        loc = ta.location
        exp = ta.elements[0].terms[0]
        attr = ta.elements[1].terms[0]
        range = ta.elements[1].condition[0]

        attr_tup = self._get_tuple(attr)
        _random = ast.Function(loc, '_random', [exp, attr_tup], False)

        body.insert(0, range)
        _random_rule = ast.Rule(loc, lit(_random), body)

        hold = ast.Function(loc, '_h', [attr_tup], False)
        attr = ast.Function(loc, attr.name, [v for v in attr.arguments], False)
        readable_to_meta = ast.Rule(loc, lit(hold), [lit(attr)])
        meta_to_readable = ast.Rule(loc, lit(attr), [lit(hold)])
        show = ast.ShowSignature(loc, attr.name, len(attr.arguments), 1, 0)
        return [_random_rule, readable_to_meta, meta_to_readable, show]

    def convert_pr(self, ta, body):
        '''
        Input:
            &pr{ r1; name(D, Y) } = "3/20"  :- body(D, Y).
        Output:
            _pr(r1, (name,D, Y), "3/20") :- body(D, Y).
        '''
        loc = ta.location
        exp = ta.elements[0].terms[0]
        attr = ta.elements[1].terms[0]
        prob = ta.guard.term

        attr_tup = self._get_tuple(attr)
        _pr = ast.Function(loc, '_pr', [exp, attr_tup, prob], False)

        _pr_rule = ast.Rule(loc, lit(_pr), body)
        return [_pr_rule]

    def convert_obs(self, ta):
        '''
        &obs { name(dom, val) ; bool}. -> _obs((name, dom, val), bool).
        &obs { name(dom, val) }.       -> _obs((name, dom, val)).
        '''
        loc = ta.location
        attr = ta.elements[0].terms[0]
        attr_tup = self._get_tuple(attr)
        body = [attr_tup]
        if len(ta.elements) > 1:
            body.append(ta.elements[1].terms[0])

        _obs = ast.Function(loc, '_obs', body, False)
        print(_obs)
        return [ast.Rule(loc, lit(_obs), [])]

    def convert_do(self, ta):
        '''
        &do { name(dom, val) }.        -> _do((name, dom, val)).
        '''
        loc = ta.location
        attr = ta.elements[0].terms[0]
        attr_tup = self._get_tuple(attr)
        _do = ast.Function(loc, '_do', [attr_tup], False)
        return [ast.Rule(loc, lit(_do), [])]
