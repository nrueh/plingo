from clingo import ast, Number


def lit(func):
    return ast.Literal(func.location, 0, ast.SymbolicAtom(func))


def calculate_weight(flt, factor):
    return Number(int(flt * (10**factor)))
