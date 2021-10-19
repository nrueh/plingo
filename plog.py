from clingo import ast


def lit(func):
    return ast.Literal(func.location, 0, ast.SymbolicAtom(func))


class ConvertPlog:
    # def __get_experiment_id(self, args):
    #     if len(args) != 0:
    #         if str(args[0].ast_type).endswith('Function'):
    #             exp_id = args[0].name
    #         elif str(args[0].ast_type).endswith('SymbolicTerm'):
    #             exp_id = args[0].symbol.name
    #     else:
    #         exp_id = ''
    #     return exp_id

    def __get_tuple(self, attr):
        loc = attr.location
        attr_name = ast.Function(loc, attr.name, [], False)
        domain_vars, range_var = attr.arguments[:-1], attr.arguments[-1]
        domain_tup = ast.Function(loc, '', domain_vars, False)
        attr_tup = ast.Function(loc, '', [attr_name, domain_tup, range_var],
                                False)
        # if exp_id == '':
        #     exp_args = [attr_name, domain_tup]
        # else:
        #     exp_id = ast.Function(loc, exp_id, [], False)
        #     exp_args = [exp_id, attr_name, domain_tup]
        exp_tup = ast.Function(loc, attr.name, [domain_tup], False)
        return attr_tup, exp_tup

    def convert_random(self, ta, body):
        '''
        Input:
            &random(r(D)) { name(D,Y) : range(Y) } :- domain(D).
                or if one random rule per attribute
            &random       { name(D,Y) : range(Y) } :- domain(D).
        Output:
            1. _random(r(D),(name,D,Y)) :- range(Y), domain(D).
                  or
               _random(name(D),(name,D,Y)) :- range(Y), domain(D).
            2. _h((name,D,Y)) :- name(D,Y).
            3. name(D,Y) :- _h((name,D,Y)).
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
        meta_to_readable = ast.Rule(loc, lit(attr), [lit(hold)])
        return [_random_rule, readable_to_meta, meta_to_readable]

    def convert_pr(self, ta, body):
        '''
        Input:
            &pr(r(D)) { name(D,Y) } = "3/20"  :- body(D,Y).
                or if one random rule per attribute
            &pr        { name(D,Y) } = "3/20"  :- body(D,Y).
        Output:
            _pr(r(D),(name,D,Y),"3/20") :- body(D,Y).
                or
            _pr(name(D),(name,D,Y),"3/20") :- body(D,Y).
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

    def convert_obs_do(self, ta):
        '''
        &obs { name(D,Y) } = bool. -> _obs((name,D,Y), bool).
            bool can be omitted and is true by default

        &do { name(D,Y) }.         -> _do((name,D,Y)).
        '''
        loc = ta.location
        attr = ta.elements[0].terms[0]
        attr_tup, _ = self.__get_tuple(attr)
        args = [attr_tup]
        if ta.term.name == 'obs':
            if ta.guard is not None:
                args.append(ta.guard.term)
            else:
                args.append(ast.Function(loc, 'true', [], False))
        _func = ast.Function(loc, f'_{ta.term.name}', args, False)
        return [ast.Rule(loc, lit(_func), [])]
