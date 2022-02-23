from clingo import Function, Number


def convert_theory_arg(arg):
    '''
    Converts the argument of a theory
    &query/1 atom to the correct Symbol.
    '''
    theory_type = str(arg.type)[15:]
    if theory_type == 'Symbol':
        return Function(arg.name)
    elif theory_type == 'Number':
        return Number(arg.number)
    elif theory_type == 'Function':
        args = [convert_theory_arg(targ) for targ in arg.arguments]
        return Function(arg.name, args)


def convert_theory_query(theory_atom):
    '''
    Converts a &query/1 atom to a Symbol.
    '''
    query_atom = theory_atom.term.arguments[0]
    name = query_atom.name
    args = []
    if query_atom.arguments != []:
        args = [convert_theory_arg(arg) for arg in query_atom.arguments]
    return Function(name, args)


def collect(queries, symbolic_atoms):
    '''
    Collects all symbolic atoms which have been queried
    through the command-line without arguments
    and combines them with other queries
    (command-line with arguments OR as theory atoms).
    '''
    # TODO: Add warning if query not present in program?
    general_queries = []
    queries_with_args = []
    for q in queries:
        if type(q) is str:
            general_queries.append(q)
        else:
            queries_with_args.append([q, []])

    query_signatures = [
        s for s in symbolic_atoms.signatures if s[0] in general_queries
    ]
    queries = queries_with_args
    for qs in query_signatures:
        for sa in symbolic_atoms.by_signature(qs[0], qs[1], qs[2]):
            if [sa.symbol, []] not in queries:
                queries.append([sa.symbol, []])
    return queries


def check_model_for_query(queries, model, model_number=None):
    '''
    Efficiently checks if a model contains a query
    and if so, saves the current model number.
    '''
    if model_number is None:
        model_number = model.number - 1
    for qa in queries:
        if model.contains(qa[0]):
            qa[1].append(model_number)
    return queries
