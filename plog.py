# from math import log

from clingo import ast, Number


def convert_random_selection_rule(plog_attributes, random_selection_rule,
                                  body):
    loc = random_selection_rule.location
    rule_name, attr, add_range = random_selection_rule.term.arguments
    if str(attr.ast_type) == 'ASTType.SymbolicTerm':
        attr = ast.Function(loc, str(attr), [], False)

    attr_name = str(attr.name)
    attr_vars = [arg for arg in attr.arguments]
    range_name = plog_attributes[str(attr_name)]['range']
    attr_domain = plog_attributes[str(attr_name)]['domain']

    # Generating rule
    # Aggregate head
    rangevar = ast.Variable(loc, 'Y')
    attr_vars.append(rangevar)
    attr_lit = ast.Literal(loc, 0,
                           ast.SymbolicAtom(attr.update(arguments=attr_vars)))

    range_lit = [
        ast.Literal(
            loc, 0,
            ast.SymbolicAtom(ast.Function(loc, range_name, [rangevar], False)))
    ]

    if str(add_range) != '()':
        if str(add_range.ast_type) == 'ASTType.SymbolicTerm':
            add_range = [str(add_range)]
        elif str(add_range.ast_type) == 'ASTType.Function':
            add_range = [str(arg) for arg in add_range.arguments]
        add_range_lit = [
            ast.Literal(
                loc, 0,
                ast.SymbolicAtom(ast.Function(loc, name, [rangevar], False)))
            for name in add_range
        ]
        range_lit.extend(add_range_lit)

    cond_lit = ast.ConditionalLiteral(loc, attr_lit, range_lit)
    agg_guard = ast.AggregateGuard(ast.ComparisonOperator.Equal,
                                   ast.SymbolicTerm(loc, Number(1)))
    head_generating_rule = ast.Aggregate(loc, agg_guard, [cond_lit], None)

    # Body
    intervene_func = ast.Function(loc, 'intervene', [attr], False)
    intervene_lit = ast.Literal(loc, 1, ast.SymbolicAtom(intervene_func))

    domain_func = [
        ast.Function(loc, attr_domain[i], [attr_vars[i]], False)
        for i in range(len(attr_domain))
    ]
    domain_lit = [
        ast.Literal(loc, 0, ast.SymbolicAtom(d)) for d in domain_func
    ]
    body.append(intervene_lit)
    body.extend(domain_lit)
    generating_rule = ast.Rule(loc, head_generating_rule, body)
    print(generating_rule)
    return [generating_rule]


def convert_attribute(plog_attributes, theory_atom):
    loc = theory_atom.location
    name, domain, attr_range = theory_atom.term.arguments
    if str(domain.ast_type) == 'ASTType.SymbolicTerm':
        domain = [str(domain)]
    else:
        domain = [str(d) for d in domain.arguments]
    plog_attributes[str(name)] = {'domain': domain, 'range': str(attr_range)}

    # Unique value for each attribute
    # -attr(D,Y1) :- attr(D,Y2), Y1 != Y2, range(Y1).
    vars = [ast.Variable(loc, f'D{i+1}') for i in range(len(domain))]
    rangevar1 = ast.Variable(loc, 'Y1')
    rangevar2 = ast.Variable(loc, 'Y2')
    vars.append(rangevar1)
    attr = ast.Function(loc, str(name), vars, False)
    negated_attr = ast.UnaryOperation(loc, ast.UnaryOperator.Minus, attr)
    negated_attr_atom = ast.SymbolicAtom(negated_attr)
    negated_attr_lit = ast.Literal(loc, 0, negated_attr_atom)
    del (vars[-1])
    vars.append(rangevar2)
    attr2 = attr.update(arguments=vars)
    attr2_lit = ast.Literal(loc, 0, ast.SymbolicAtom(attr2))
    comparison = ast.Literal(
        loc, 0,
        ast.Comparison(ast.ComparisonOperator.NotEqual, rangevar1, rangevar2))
    range_lit1 = ast.Literal(
        loc, 0,
        ast.SymbolicAtom(ast.Function(loc, str(attr_range), [rangevar1],
                                      False)))
    unique_attr_rule = ast.Rule(loc, negated_attr_lit,
                                [attr2_lit, comparison, range_lit1])

    # Fixed attributes will not be considered random
    # intervene(attr(D)) :- do(attr(D,Y)).
    do_func = ast.Function(loc, 'do', [attr], False)
    do_func = ast.Literal(loc, 0, ast.SymbolicAtom(do_func))
    del (vars[-1])
    intervene_func = ast.Function(loc, 'intervene',
                                  [attr.update(arguments=vars)], False)
    intervene_func = ast.Literal(loc, 0, ast.SymbolicAtom(intervene_func))
    fixed_attr_rule = ast.Rule(loc, intervene_func, [do_func])

    # Observations have to be true in the answer set
    # :- obs(attr(D,Y)), not attr(D,Y).
    # :- obs(-attr(D,Y)), not -attr(D,Y).
    obs_positive_lit = ast.Literal(
        loc, 0, ast.SymbolicAtom(ast.Function(loc, 'obs', [attr], False)))
    obs_negative_lit = ast.Literal(
        loc, 0,
        ast.SymbolicAtom(ast.Function(loc, 'obs', [negated_attr], False)))

    attr_atom = ast.SymbolicAtom(attr)
    not_attr = ast.Literal(loc, 1, attr_atom)
    not_negated_attr = ast.Literal(loc, 1, negated_attr_atom)

    int_constraint_head = ast.Literal(loc, 0, ast.BooleanConstant(False))

    constraint_positive_obs = ast.Rule(loc, int_constraint_head,
                                       [obs_positive_lit, not_attr])
    constraint_negative_obs = ast.Rule(loc, int_constraint_head,
                                       [obs_negative_lit, not_negated_attr])

    # Actions make literals true
    # attr(D,Y) :- do(attr(D,Y)).
    actions_make_true_rule = ast.Rule(loc, ast.Literal(loc, 0, attr_atom),
                                      [do_func])
    return [
        unique_attr_rule, fixed_attr_rule, constraint_negative_obs,
        constraint_positive_obs, actions_make_true_rule
    ]
