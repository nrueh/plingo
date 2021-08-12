import argparse
import os

parser = argparse.ArgumentParser(description='Generate grid of size s.')
parser.add_argument('--query', '-q', type=int, help='Diagonal node to query')

args = parser.parse_args()


def generate_graph(gridsize, prob):
    program = []
    for i in range(1, gridsize + 1):
        for j in range(1, gridsize + 1):
            if i < gridsize:
                program.append(f'{prob}::edge(n_{i}_{j},n_{i+1}_{j}).')
            if j < gridsize:
                program.append(f'{prob}::edge(n_{i}_{j},n_{i}_{j+1}).')
            if i < gridsize and j < gridsize:
                program.append(f'{prob}::edge(n_{i}_{j+1},n_{i}_{j+1}).')
    program.append('')
    program.append('path(X,Y) :- edge(X,Y).')
    program.append('path(X,Y) :- edge(X,Z), path(Z,Y).')
    program.append('')
    program.append(f'query(path(n_{args.query}_{args.query},n_16_16)).')
    return program


if __name__ == '__main__':
    prob = 0.5
    gridsize = 16
    program = generate_graph(gridsize, prob)
    outdir = 'grids'
    filename = f'query{args.query}.pl'

    with open(os.path.join(outdir, filename), 'w') as f:
        f.write('\n'.join(program))
