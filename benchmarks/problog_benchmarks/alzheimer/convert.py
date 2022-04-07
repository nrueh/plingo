import argparse
import os
from math import log

parser = argparse.ArgumentParser(
    description=
    'convert Alzheimer benchmark instances between ProbLog, plingo and LPMLN format.'
)
parser.add_argument('--input', '-i', type=str, help='input folder')
parser.add_argument('--output',
                    '-o',
                    choices=['problog', 'lpmln', 'plingo'],
                    help='output format')

args = parser.parse_args()


def parse_lpmln(line):
    return None, None


def parse_plingo(line):
    edge, prob = line.split(':-')
    edge = edge.strip()
    prob = prob[prob.index('(') + 1:prob.index(')')]
    return edge, prob


if __name__ == '__main__':
    instances = os.listdir(args.input)
    outdir = f'instances_{args.output}'
    os.makedirs(outdir)
    for instance in instances:
        print(instance)
        with open(os.path.join(args.input, instance), 'r') as fp:
            lines = fp.read().strip().split('\n')

        new_program = []
        for line in lines[:-6]:
            line = line.strip()
            if line == '' or line[0] == '%':
                continue
            if 'problog' in args.input:
                prob, edge = line.split('::')
                edge = edge[:-1]
            elif 'lpmln' in args.input:
                prob, edge = parse_lpmln(line)
            elif 'plingo' in args.input:
                prob, edge = parse_plingo(line)
            else:
                raise ValueError('Input format not recognized')

            if args.output == 'problog':
                new_rule = f'{prob}::{edge}.'
            elif args.output == 'lpmln':
                edge = edge.replace('\'', '"')
                prob = log(float(prob) / (1 - float(prob)))
                new_rule = f'{prob}  {edge}.'
            elif args.output == 'plingo':
                edge = edge.replace('\'', '"')
                new_rule = f'{edge} :- &problog("{prob}").'
            new_program.append(new_rule)

        file_ending = '.lp'
        if args.output == 'problog':
            new_program.append('p(X,Y) :- drc(X,Y).')
            new_program.append('p(X,Y) :- drc(X, Z), Z \\= Y, p(Z, Y).')
            new_program.append("query :- p('hgnc_582', 'hgnc_983').")
            new_program.append('query(query).')
            file_ending = '.pl'

        new_instance_name = instance.split('.')[0] + file_ending

        outpath = os.path.join(outdir, new_instance_name)
        new_program = '\n'.join(new_program)

        with open(outpath, 'w') as fp:
            fp.write(new_program)
