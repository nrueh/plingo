import os
import json
import time

from clingo import clingo_main
from no_theory_lpmln import LPMLNApp


def get_parameters(filename):
    filename = filename.split('_')
    num_nodes = int(filename[0][1:])
    if len(filename) == 2:
        p = int(filename[1][1:-3])
    else:
        p = int(filename[1][1:])
    return num_nodes, p


if __name__ == '__main__':
    instance_dir = 'benchmarks/random_graphs/'
    graph_instances = os.listdir(instance_dir)
    graph_instances.sort(
        key=lambda x: (get_parameters(x)[0], get_parameters(x)[1]))

    running_times = {}

    for idx, g in enumerate(graph_instances):
        num_nodes, p = get_parameters(g)
        graph_path = os.path.join(instance_dir, g)
        current_files = [
            'benchmarks/relaxed_clique.lpmln', graph_path, '--outf=3'
        ]
        start = time.time()
        exit_code = clingo_main(LPMLNApp(), current_files)
        end = time.time()

        running_times[str(idx)] = {
            'N': num_nodes,
            'p': p,
            'time': end - start,
            'file': g
        }
        with open('running_times.json', 'w') as fp:
            json.dump(running_times, fp)

        print(f'\n Num. nodes: {num_nodes}, probability: {p}')
        print(end - start)
