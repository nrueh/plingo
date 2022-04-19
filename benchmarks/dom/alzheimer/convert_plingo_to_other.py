import argparse
from math import log
parser = argparse.ArgumentParser(
    description='Convert a file in Plingo syntax to ProbLog or azreasoners syntax.')
parser.add_argument('--target', '-t', type=str, help='Should be \'problog\' or \'az\'')
parser.add_argument('--file', '-f', type=str, help='Plingo file')
parser.add_argument('--output', '-o', type=str, help='Output file path')
args = parser.parse_args()


def get_head_body(line):
    head, body = line.split(':-')
    head = head.strip()
    body = body.strip()[:-1].split(',')
    return head, body


if __name__ == '__main__':
    with open(args.file, 'r') as fp:
        lines = fp.readlines()

    problog_program = []

    for line in lines:
        line = line.strip()
        # if line == '' or line[0] == '%':
        #     continue
        separator = '  '
        if args.target == 'problog':
            separator = '::'
            line = line.replace('!=', '\=')

        if '&problog' in line:
            head, body = get_head_body(line)
            probability = [b for b in body if '&problog' in b][0]
            body.remove(probability)
            probability = probability.replace('&problog("', '')[:-2]
            probability = probability.strip()
            if args.target == 'az':
                probability = float(probability) / (1-float(probability))
            problog_fact = f'{probability}{separator}{head}{" :- " if len(body) != 0 else ""}{",".join(body)}.'
            problog_program.append(problog_fact)
        elif '&query' in line:
            if args.target == 'problog':
                problog_program.append(line[1:])
        else:
            problog_program.append(line)

    with open(args.output, 'w') as fp:
        fp.write('\n'.join(problog_program))
