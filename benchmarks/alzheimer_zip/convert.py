import argparse
import os
from math import log
from shutil import copytree

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
    prob = prob[prob.index('(') + 2:prob.index(')') - 1]
    return prob, edge


if __name__ == '__main__':
    instances = os.listdir(args.input)
    outdir = f'instances_{args.output}'
    if os.path.isdir(outdir):
        res = input(f'Directory {outdir} exists already. Continue? y/n  ')
        if res not in ['yes', 'y', 'Yes', 'Y']:
            quit()
        copytree(outdir, '.backup_instances', dirs_exist_ok=True)
        os.makedirs(outdir, exist_ok=True)

    for instance in instances:
        if instance.endswith('.py') or instance in [
                'encoding.lp', 'evidence.lp', 'query.lp'
        ]:
            continue
        print(instance)
        with open(os.path.join(args.input, instance), 'r') as fp:
            lines = fp.read().strip().split('\n')
        if 'problog' in args.input:
            lines = [l for l in lines if '::' in l]

        new_program = []
        for line in lines:
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
                edge = edge.replace('"', '\'')
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
            # new_program.append("query :- p('hgnc_582', 'hgnc_983').")
            # new_program.append('query(query).')
            file_ending = '.pl'
        new_program.append('')
        new_instance_name = instance.split('.')[0] + file_ending

        outpath = os.path.join(outdir, new_instance_name)
        new_program = '\n'.join(new_program)

        with open(outpath, 'w') as fp:
            fp.write(new_program)
