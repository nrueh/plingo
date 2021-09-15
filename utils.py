from clingo import ast, Number


def lit(func):
    return ast.Literal(func.location, 0, ast.SymbolicAtom(func))


def calculate_weight(f):
    return Number(int(f * (10**5)))
