import argparse
import random
import os

parser = argparse.ArgumentParser(
    description=
    'Generate random graph with n nodes and probability p to generate an edge.'
)
parser.add_argument('--num_nodes', '-n', type=int, help='Number of nodes')

args = parser.parse_args()


def generate_graph(num_nodes, prob):
    program = []
    for i in range(num_nodes):
        program.append(f'node({i}).')
        for j in range(i + 1, num_nodes):
            if random.random() < prob:
                program.append(f'edge({i}, {j}).')
                program.append(f'edge({j}, {i}).')
    return program


if __name__ == '__main__':
    random.seed(31)
    outdir = 'benchmarks/random_graphs'

    probs = [0.5, 0.8, 0.9, 1.0]

    for p in probs:
        program = generate_graph(args.num_nodes, p)
        filename = f'N{args.num_nodes}_p{int(p*100)}.lp'

        with open(os.path.join(outdir, filename), 'w') as f:
            f.write('\n'.join(program))
