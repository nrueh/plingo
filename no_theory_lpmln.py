import sys

import clingo

# THEORY = """
# #theory lpmln{
#     diff_term {
#     -  : 3, unary;
#     ** : 2, binary, right;
#     *  : 1, binary, left;
#     /  : 1, binary, left;
#     \\ : 1, binary, left;
#     +  : 0, binary, left;
#     -  : 0, binary, left
#     };
#     &diff/1 : weight, {::}, rule, any
# }
# """˚


def parse_lpmln(file):
    with open(file, 'r') as fp:
        lines = fp.read().splitlines()

    ctl = clingo.Control()

    for rule in lines:
        rule = rule.strip()

        # Skip comments
        if rule[0] == '%':
            continue

        if '::' in lpmln_rule:
            split = lpmln_rule.split('::')
            weight = int(split[0])
            lpmln_rule = split[1][1:]
            # print('weight: ' + str(weight))

        # conversion LP^MLN to ASP with weak constraints
        asp_rule1 = ""
        ctl.add("base", [], rule)

    ctl.ground([("base", [])])
    ctl.solve(on_model=print)


if __name__ == '__main__':
    files = sys.argv[1:]
    print(files)

    parse_lpmln(files[0])
