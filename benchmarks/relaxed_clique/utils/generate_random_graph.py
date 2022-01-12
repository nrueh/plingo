import argparse
import random
import os

# parser = argparse.ArgumentParser(
#     description=
#     'Generate random graph with n nodes and probability p to generate an edge.'
# )
# parser.add_argument('--num_nodes', '-n', type=int, help='Number of nodes')

# args = parser.parse_args()


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
    # random.seed(31)
    outdir = 'random_graphs_oneside'

    probs = [0.5, 0.8, 0.9, 1.0]
    nodes = [5, 10, 20, 50, 100, 200, 500, 1000]
    for n in nodes:
        for p in probs:
            program = generate_graph(n, p)
            filename = f'N{n}_p{int(p*100)}.lp'
            outpath = os.path.join(outdir, filename)
            counter = 0
            while os.path.exists(outpath):
                filename = f'N{n}_p{int(p*100)}_{counter}.lp'
                outpath = os.path.join(outdir, filename)
                counter += 1

            with open(outpath, 'w') as f:
                f.write('\n'.join(program))
