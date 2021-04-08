import json

import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    json_file = 'running_times.json'

    with open(json_file, 'r') as fp:
        benchmarks = json.load(fp)

    probs = [50, 80, 90, 100]
    plt.figure()
    for p in probs:
        num_nodes = []
        times = []
        for k in benchmarks.keys():
            current_entry = benchmarks[k]
            if current_entry['p'] == p:
                num_nodes.append(current_entry['N'])
                times.append(current_entry['time'])
        plt.plot(num_nodes, times, label=f'p={p/100}', marker='+',
                 ms=4)  #, s=20, marker='x')
    plt.legend(loc='upper left')
    #plt.yscale('log')
    plt.ylim([-10, 150])
    plt.title('Benchmark: Maximal relaxed clique')
    plt.xlabel('Number of nodes')
    plt.ylabel('Running times in seconds')
    plt.savefig('max_relaxed_clique.png', dpi=600)