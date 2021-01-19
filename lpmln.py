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
        
        if '::' in rule:
            split = rule.split('::')
            weight = int(split[0])
            rule = split[1][1:]
            # print('weight: ' + str(weight))

        ctl.add("base", [], rule)
    
    ctl.ground([("base", [])])
    ctl.solve(on_model=print)


if __name__ == '__main__':
    files = sys.argv[1:]
    print(files)

    parse_lpmln(files[0])