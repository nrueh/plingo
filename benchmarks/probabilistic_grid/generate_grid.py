import argparse
import os

parser = argparse.ArgumentParser(description='Generate grid of size s.')
parser.add_argument('--gridsize', '-s', type=int, help='Number of nodes')

args = parser.parse_args()


def generate_graph(gridsize, prob):
    program = []
    for i in range(1, gridsize + 1):
        for j in range(1, gridsize + 1):
            if i < gridsize:
                program.append(
                    f'edge(n_{i}_{j},n_{i+1}_{j}) :- &log(\"{prob/(1-prob)}\").'
                )
                # program.append(
                #     f':- edge(n_{i}_{j},n_{i+1}_{j}), &log(\"{1-prob}\").')
            if j < gridsize:
                program.append(
                    f'edge(n_{i}_{j},n_{i}_{j+1}) :- &log(\"{prob/(1-prob)}\").'
                )
                # program.append(
                #     f':- edge(n_{i}_{j},n_{i}_{j+1}), &log(\"{1-prob}\").')
            if i < gridsize and j < gridsize:
                program.append(
                    f'edge(n_{i}_{j},n_{i+1}_{j+1}) :- &log(\"{prob/(1-prob)}\").'
                )
                # program.append(
                #     f':- edge(n_{i}_{j},n_{i+1}_{j+1}), &log(\"{1-prob}\").')
    return program


if __name__ == '__main__':
    prob = 0.5
    gridsize = args.gridsize
    program = generate_graph(gridsize, prob)
    outdir = 'grids'
    filename = f'grid{gridsize}.lp'

    with open(os.path.join(outdir, filename), 'w') as f:
        f.write('\n'.join(program))

    with open(os.path.join(outdir, f'evid{gridsize}.lp'), 'w') as f:
        f.write(f':- not path(n_1_1, n_{gridsize}_{gridsize}).')
