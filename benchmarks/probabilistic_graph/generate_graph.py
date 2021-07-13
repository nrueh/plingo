import argparse
import random
import os

parser = argparse.ArgumentParser(
    description='Generate random graph with n edges with probability p.')
parser.add_argument('--num_edges', '-n', type=int, help='Number of edges')

args = parser.parse_args()


def generate_graph(num_nodes, prob):
    program = []
    for i in range(num_nodes):
        program.append(f'node({i}).')
        for j in range(i + 1, num_nodes):
            if random.random() < prob:
                program.append(f'edge({i}, {j}).')
                # program.append(f'edge({j}, {i}).')
    return program


if __name__ == '__main__':
    program = []
    for i in range(args.num_edges):
        prob = 0
        while prob == 0:
            prob = random.random()
        prob = prob / (1 - prob)

        program.append(f'edge({i}, {i+1}) :- &log(\"{prob}\").')
    #     program.append(f':- edge(n_{i}_{j},n_{i+1}_{j}), &log(\"0.5\").')
    filename = f'sequential{args.num_edges}.lp'

    outdir = 'graphs'
    outfile = os.path.join(outdir, filename)
    with open(outfile, 'w') as f:
        f.write('\n'.join(program))

    # with open(os.path.join(outdir, f'sequential_evid{args.num_edges}.lp'),
    #           'w') as f:
    #     f.write(f':- not path(1,{args.num_edges}).')
