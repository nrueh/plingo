# from math import log

from clingo import ast

from utils import lit


class ConvertPlog:
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

        # # Weak constraint for default probability
        # # :~ not numdefprob(attribute(Name, Domain), M), cardinality_numdefprob(M),
        # #       posswithdefprob(attribute(Name, Domain, _)). [log((1/M))@0,Name,Domain]
        # vars = [ast.Variable(loc, 'Name'), ast.Variable(loc, 'Domain')]
        # meta_attr2 = ast.Function(loc, 'attribute', vars, False)

        # vars.append(ast.Variable(loc, '_'))
        # meta_attr3 = ast.Function(loc, 'attribute', vars, False)
        # priority = ast.SymbolicTerm(loc, Number(0))

        # for m in range(2, len(terms.arguments) + 1):
        #     defprob_weight = ast.SymbolicTerm(loc, calculate_weight(log(1 / m)))
        #     m_term = ast.SymbolicTerm(loc, Number(m))
        #     cardinality = ast.Function(loc, 'cardinality_numdefprob', [m_term],
        #                                False)
        #     notnumdefprob_func = ast.Function(loc, 'numdefprob',
        #                                       [meta_attr2, m_term], False)
        #     notnumdefprob_lit = ast.Literal(loc, 1,
        #                                     ast.SymbolicAtom(notnumdefprob_func))
        #     posswithdefprob = ast.Function(loc, 'posswithdefprob', [meta_attr3],
        #                                    False)
        #     defaultprob_wc = ast.Minimize(
        #         loc, defprob_weight, priority, [meta_attr2],
        #         [notnumdefprob_lit,
        #          lit(cardinality),
        #          lit(posswithdefprob)])
        #     asp_rules.append(defaultprob_wc)

        return [sort_fact, meta_to_readable]

    def convert_attribute(self, theory_atom):
        loc = theory_atom.location
        attr_name, domain, attr_range = theory_atom.term.arguments
        if str(domain.ast_type) == 'ASTType.SymbolicTerm':
            domain = [str(domain)]
        else:
            domain = [str(d) for d in domain.arguments]

        # Create meta attribute facts
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

        if str(attr_range) == 'boolean':
            range_var = None
            range_sort = ast.Function(loc, '', [], False)
        else:
            range_var = ast.Variable(loc, 'Y')
            range_sort = ast.Function(
                loc, 'sort',
                [ast.Function(loc, str(attr_range), [], False), range_var],
                False)

        meta_attr_func = ast.Function(loc, 'attribute',
                                      [name_func, domain_func, range_sort],
                                      False)
        meta_attr_rule_body = [lit(ds) for ds in domain_sort]
        if str(attr_range) != 'boolean':
            meta_attr_rule_body.insert(0, lit(range_sort))
        meta_attr_rule = ast.Rule(loc, lit(meta_attr_func),
                                  meta_attr_rule_body)

        # Conversion between meta and readable for positive attributes
        if range_var is not None:
            domain_vars.append(range_var)
        attr = ast.Function(loc, str(attr_name), domain_vars, False)
        hold_func = ast.Function(loc, 'hold', [meta_attr_func], False)
        meta_to_readable_pos = ast.Rule(loc, lit(attr), [lit(hold_func)])
        readable_to_meta_pos = ast.Rule(loc, lit(hold_func), [lit(attr)])

        # Convert between meta and readable for negative attributes
        negated_attr = ast.UnaryOperation(loc, ast.UnaryOperator.Minus, attr)
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

        # # Unique value for each attribute
        # # -attr(D,Y1) :- attr(D,Y2), Y1 != Y2, range(Y1).
        # vars = [ast.Variable(loc, f'D{i+1}') for i in range(len(domain))]
        # rangevar1 = ast.Variable(loc, 'Y1')
        # rangevar2 = ast.Variable(loc, 'Y2')
        # vars.append(rangevar1)
        # attr = ast.Function(loc, str(name), vars, False)
        # negated_attr = ast.UnaryOperation(loc, ast.UnaryOperator.Minus, attr)
        # negated_attr_atom = ast.SymbolicAtom(negated_attr)
        # negated_attr_lit = ast.Literal(loc, 0, negated_attr_atom)
        # del (vars[-1])
        # vars.append(rangevar2)
        # attr2 = attr.update(arguments=vars)
        # attr2_lit = ast.Literal(loc, 0, ast.SymbolicAtom(attr2))
        # comparison = ast.Literal(
        #     loc, 0,
        #     ast.Comparison(ast.ComparisonOperator.NotEqual, rangevar1, rangevar2))
        # range_lit1 = ast.Literal(
        #     loc, 0,
        #     ast.SymbolicAtom(ast.Function(loc, str(attr_range), [rangevar1],
        #                                   False)))
        # unique_attr_rule = ast.Rule(loc, negated_attr_lit,
        #                             [attr2_lit, comparison, range_lit1])

        # # Fixed attributes will not be considered random
        # # intervene(attr(D)) :- do(attr(D,Y)).
        # do_func = ast.Function(loc, 'do', [attr], False)
        # do_func = ast.Literal(loc, 0, ast.SymbolicAtom(do_func))
        # del (vars[-1])
        # intervene_func = ast.Function(loc, 'intervene',
        #                               [attr.update(arguments=vars)], False)
        # intervene_func = ast.Literal(loc, 0, ast.SymbolicAtom(intervene_func))
        # fixed_attr_rule = ast.Rule(loc, intervene_func, [do_func])

        # # Observations have to be true in the answer set
        # # :- obs(attr(D,Y)), not attr(D,Y).
        # # :- obs(-attr(D,Y)), not -attr(D,Y).
        # obs_positive_lit = ast.Literal(
        #     loc, 0, ast.SymbolicAtom(ast.Function(loc, 'obs', [attr], False)))
        # obs_negative_lit = ast.Literal(
        #     loc, 0,
        #     ast.SymbolicAtom(ast.Function(loc, 'obs', [negated_attr], False)))

        # attr_atom = ast.SymbolicAtom(attr)
        # not_attr = ast.Literal(loc, 1, attr_atom)
        # not_negated_attr = ast.Literal(loc, 1, negated_attr_atom)

        # int_constraint_head = ast.Literal(loc, 0, ast.BooleanConstant(False))

        # constraint_positive_obs = ast.Rule(loc, int_constraint_head,
        #                                    [obs_positive_lit, not_attr])
        # constraint_negative_obs = ast.Rule(loc, int_constraint_head,
        #                                    [obs_negative_lit, not_negated_attr])

        # # Actions make literals true
        # # attr(D,Y) :- do(attr(D,Y)).
        # actions_make_true_rule = ast.Rule(loc, ast.Literal(loc, 0, attr_atom),
        #                                   [do_func])
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

        # # Weak constraint for assigned probability
        # # :~ not assprob(RandomIdentifier, Attr), pratom(RandomIdentifier, Attr, Prob). [log(Prob)@0,RandomIdentifier,Attr]
        # assprob_weight = ast.SymbolicTerm(
        #     loc, calculate_weight(log(eval(prob.symbol.string))))

        # notassprob_func = ast.Function(loc, 'assprob',
        #                                [random_identifier, meta_attr], False)
        # notassprob_lit = ast.Literal(loc, 1, ast.SymbolicAtom(notassprob_func))
        # assprob_wc = ast.Minimize(loc, assprob_weight,
        #                           ast.SymbolicTerm(loc, Number(0)),
        #                           [random_identifier, meta_attr],
        #                           [notassprob_lit, lit(pratom)])

        # # :~ not totaldefprob(Attr2, X), remprob(Attr2, X). [@log(@frac(X,100))@0]

        return [pratom_rule]

    # def convert_random_selection_rule(attributes, random_selection_rule, body):
    #     loc = random_selection_rule.location
    #     rule_name, attr, set_term = random_selection_rule.term.arguments
    #     if str(attr.ast_type) == 'ASTType.SymbolicTerm':
    #         attr = ast.Function(loc, str(attr), [], False)

    #     attr_name = str(attr.name)
    #     attr_vars = [arg for arg in attr.arguments]
    #     range_name = attributes[str(attr_name)]['range']
    #     attr_domain = attributes[str(attr_name)]['domain']

    #     # Generating rule
    #     # Aggregate head
    #     rangevar = ast.Variable(loc, 'Y')
    #     attr_vars.append(rangevar)
    #     attr_lit = ast.Literal(loc, 0,
    #                            ast.SymbolicAtom(attr.update(arguments=attr_vars)))

    #     range_lit = [
    #         ast.Literal(
    #             loc, 0,
    #             ast.SymbolicAtom(ast.Function(loc, range_name, [rangevar], False)))
    #     ]

    #     if str(set_term) != '()':
    #         if str(set_term.ast_type) == 'ASTType.SymbolicTerm':
    #             set_term = [str(set_term)]
    #         elif str(set_term.ast_type) == 'ASTType.Function':
    #             set_term = [str(arg) for arg in set_term.arguments]
    #         set_term_lit = [
    #             ast.Literal(
    #                 loc, 0,
    #                 ast.SymbolicAtom(ast.Function(loc, name, [rangevar], False)))
    #             for name in set_term
    #         ]
    #         range_lit.extend(set_term_lit)

    #     cond_lit = ast.ConditionalLiteral(loc, attr_lit, range_lit)
    #     agg_guard = ast.AggregateGuard(ast.ComparisonOperator.Equal,
    #                                    ast.SymbolicTerm(loc, Number(1)))
    #     head_generating_rule = ast.Aggregate(loc, agg_guard, [cond_lit], None)

    #     # Body
    #     intervene_func = ast.Function(loc, 'intervene', [attr], False)
    #     intervene_lit = ast.Literal(loc, 1, ast.SymbolicAtom(intervene_func))

    #     domain_func = [
    #         ast.Function(loc, attr_domain[i], [attr_vars[i]], False)
    #         for i in range(len(attr_domain))
    #     ]
    #     domain_lit = [
    #         ast.Literal(loc, 0, ast.SymbolicAtom(d)) for d in domain_func
    #     ]
    #     body.append(intervene_lit)
    #     body.extend(domain_lit)
    #     generating_rule = ast.Rule(loc, head_generating_rule, body)

    #     # Possible atoms
    #     return [generating_rule]
