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

    def convert_sort(self, theory_atom):
        loc = theory_atom.location
        name, terms = theory_atom.term.arguments

        # sort(Name, (X1;X2;X3;)).
        sort_func = ast.Function(loc, 'sort', [name, terms], False)
        sort_fact = ast.Rule(loc, lit(sort_func), [])

        # Name(X) :- sort(Name, X).
        var = ast.Variable(loc, 'X')
        head_func = ast.Function(loc, str(name), [var], False)
        body_func = ast.Function(loc, 'sort', [name, var], False)
        meta_to_readable = ast.Rule(loc, lit(head_func), [lit(body_func)])
        return [sort_fact, meta_to_readable]

    def convert_setterm(self, theory_atom):
        # Conversion between meta hold statements and readable
        # setterm(Y) :- hold(setterm, sort(Range, Y))
        # hold(setterm, sort(Range, Y)) :- setterm(Y)
        loc = theory_atom.location
        name, range_name = theory_atom.term.arguments
        range_var = ast.Variable(loc, 'Y')
        range_sort = ast.Function(loc, 'sort', [range_name, range_var], False)
        hold_func = ast.Function(loc, 'hold', [name, range_sort], False)
        setterm_func = ast.Function(loc, str(name), [range_var], False)

        meta_to_readable = ast.Rule(loc, lit(setterm_func), [lit(hold_func)])
        readable_to_meta = ast.Rule(loc, lit(hold_func), [lit(setterm_func)])
        return meta_to_readable, readable_to_meta

    def convert_attribute(self, theory_atom):
        loc = theory_atom.location
        attr_name, domain, attr_range = theory_atom.term.arguments
        if str(domain.ast_type) == 'ASTType.SymbolicTerm':
            domain = [str(domain)]
        else:
            domain = [str(d) for d in domain.arguments]

        # Create meta attribute facts
        # attribute(name, domain(Domain, D), sort(Range, Y))
        name_func = ast.Function(loc, str(attr_name), [], False)

        domain_vars = [
            ast.Variable(loc, f'D{i+1}') for i in range(len(domain))
        ]
        domain_sort = [
            ast.Function(
                loc, 'sort',
                [ast.Function(loc, domain[i], [], False), domain_vars[i]],
                False) for i in range(len(domain))
        ]
        domain_func = ast.Function(loc, 'domain', domain_sort, False)

        range_var = ast.Variable(loc, 'Y')
        range_sort = ast.Function(
            loc, 'sort',
            [ast.Function(loc, str(attr_range), [], False), range_var], False)

        meta_attr_func = ast.Function(loc, 'attribute',
                                      [name_func, domain_func, range_sort],
                                      False)
        meta_attr_rule_body = [lit(ds) for ds in domain_sort]
        meta_attr_rule_body.insert(0, lit(range_sort))
        meta_attr_rule = ast.Rule(loc, lit(meta_attr_func),
                                  meta_attr_rule_body)

        # Conversion between meta hold terms and readable for positive attributes
        if range_var is not None:
            domain_vars.append(range_var)
        attr = ast.Function(loc, str(attr_name), domain_vars, False)
        hold_func = ast.Function(loc, 'hold', [meta_attr_func], False)
        meta_to_readable_pos = ast.Rule(loc, lit(attr), [lit(hold_func)])
        readable_to_meta_pos = ast.Rule(loc, lit(hold_func), [lit(attr)])

        # Convert between meta hold terms and readable for negative attributes
        negated_attr = ast.UnaryOperation(loc, ast.UnaryOperator.Minus, attr)

        if range_var is not None:
            del (domain_vars[-1])
        negated_hold = ast.UnaryOperation(loc, ast.UnaryOperator.Minus,
                                          hold_func)
        meta_to_readable_neg = ast.Rule(loc, lit(negated_attr),
                                        [lit(negated_hold)])
        readable_to_meta_neg = ast.Rule(loc, lit(negated_hold),
                                        [lit(negated_attr)])

        # Rule for obs conversion
        obs_meta_func_pos = ast.Function(loc, 'obs', [hold_func], False)
        obs_func_pos = ast.Function(loc, 'obs', [attr], False)
        pos_obs = ast.Rule(
            loc, lit(obs_meta_func_pos),
            [lit(obs_func_pos), lit(meta_attr_func)])

        obs_meta_func_neg = ast.Function(loc, 'obs', [negated_hold], False)
        obs_func_neg = ast.Function(loc, 'obs', [negated_attr], False)
        neg_obs = ast.Rule(
            loc, lit(obs_meta_func_neg),
            [lit(obs_func_neg), lit(meta_attr_func)])

        # Rules for do conversion
        do_meta_func_pos = ast.Function(loc, 'do', [hold_func], False)
        do_func_pos = ast.Function(loc, 'do', [attr], False)
        pos_do = ast.Rule(
            loc, lit(do_meta_func_pos),
            [lit(do_func_pos), lit(meta_attr_func)])

        do_meta_func_neg = ast.Function(loc, 'do', [negated_hold], False)
        do_func_neg = ast.Function(loc, 'do', [negated_attr], False)
        neg_do = ast.Rule(
            loc, lit(do_meta_func_neg),
            [lit(do_func_neg), lit(meta_attr_func)])
        return [
            meta_attr_rule, meta_to_readable_pos, readable_to_meta_pos,
            meta_to_readable_neg, readable_to_meta_neg, pos_obs, neg_obs,
            pos_do, neg_do
        ]

    def convert_pratom(self, pratom, body):
        loc = pratom.location
        random_identifier, attr, prob = pratom.term.arguments

        # Create pratom rule
        name_func = ast.Function(loc, attr.name, [], False)
        pr_domain = attr.arguments[:-1]
        pr_range = attr.arguments[-1]

        domain_vars = [
            ast.Variable(loc, f'Domain{i+1}') for i in range(len(pr_domain))
        ]
        domain_sort = [
            ast.Function(loc, 'sort', [domain_vars[i], pr_domain[i]], False)
            for i in range(len(pr_domain))
        ]
        domain_func = ast.Function(loc, 'domain', domain_sort, False)

        range_var = ast.Variable(loc, 'Range')
        range_sort = ast.Function(loc, 'sort', [range_var, pr_range], False)
        meta_attr = ast.Function(loc, 'attribute',
                                 [name_func, domain_func, range_sort], False)
        pratom = ast.Function(loc, 'pratom',
                              [random_identifier, meta_attr, prob], False)
        body.insert(0, lit(meta_attr))
        pratom_rule = ast.Rule(loc, lit(pratom), body)
        print(pratom_rule)
        return [pratom_rule]

    def convert_random(self, ta, body):
        '''
        Input:
            &random{ r1; name(D,Y) : range(Y) } :- domain(D).
        Output:
            _random(r1,(name,D,Y)) :- range(Y), domain(D).
            _h((name,D,Y)) :- name(D,Y).
            name(D,Y) :- _h((name,D,Y)).
            #show name/X. (X: arity of name(D,Y) atom)
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
            &pr{ r1; name(D,Y) } = "3/20"  :- body(D,Y).
        Output:
            _pr(r1,(name,D,Y),"3/20") :- body(D,Y).
        '''
        loc = ta.location
        exp = ta.elements[0].terms[0]
        attr = ta.elements[1].terms[0]
        prob = ta.guard.term

        attr_tup = self._get_tuple(attr)
        _pr = ast.Function(loc, '_pr', [exp, attr_tup, prob], False)

        _pr_rule = ast.Rule(loc, lit(_pr), body)
        return [_pr_rule]
