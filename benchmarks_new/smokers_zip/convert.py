import argparse
import os
from math import log
from shutil import copytree

parser = argparse.ArgumentParser(
    description=
    'convert Smokers benchmark instances between ProbLog, plingo and LPMLN format.'
)
parser.add_argument('--input', '-i', type=str, help='input folder')
parser.add_argument('--output',
                    '-o',
                    choices=['problog', 'lpmln', 'plingo'],
                    help='output format')

args = parser.parse_args()


def parse_people(line):
    if 'problog' in args.input:
        sep = ['[', ']', ',']
    elif 'lpmln' in args.input:
        sep = ['(', ')', ';']
    elif 'plingo' in args.input:
        sep = ['(', ')', ';']
    people = line[line.index(sep[0]) + 1:line.index(sep[1])].split(sep[2])
    if args.output == 'problog':
        return f'people([{",".join(people)}]).'
    elif args.output == 'lpmln' or args.output == 'plingo':
        return f'people({";".join(people)}).'


if __name__ == '__main__':
    instances = os.listdir(args.input)
    outdir = os.path.join(f'instances_{args.output}', 'instances')
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

        new_program = []
        for line in lines:
            if 'kb_smokes' in line:
                continue
            line = line.strip()
            if line == '' or line[0] == '%':
                continue
            elif line.startswith('friend'):
                new_program.append(line)
            elif line.startswith('people'):
                new_program.append(parse_people(line))
            elif 'evidence' in line or 'query' in line:
                if args.output == 'plingo':
                    new_program.append('&' + line)
            else:
                raise Exception('Unknown type')

        file_ending = '.pl' if args.output == 'problog' else '.lp'
        new_program.append('')
        new_instance_name = instance.split('.')[0] + file_ending

        outpath = os.path.join(outdir, new_instance_name)
        new_program = '\n'.join(new_program)
        print(outpath)
        with open(outpath, 'w') as fp:
            fp.write(new_program)
