import argparse
import json

import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='Plot benchmark results.')
parser.add_argument('--csv_file',
                    '-c',
                    type=str,
                    help='CSV file containing benchmark results')
parser.add_argument('--outfile', '-o', type=str, help='Path to save plot')
parser.add_argument('--system',
                    '-s',
                    type=str,
                    help="Which system was used (ours or azreasoners)")
args = parser.parse_args()

if __name__ == '__main__':
    # json_file = 'running_times.json'

    # with open(json_file, 'r') as fp:
    # benchmarks = json.load(fp)
    data = np.genfromtxt(args.csv_file,
                         delimiter=" ",
                         dtype=None,
                         encoding=None)
    # timeout_rows = np.argwhere(data == 'timeout')[:, 0]
    data[np.argwhere(data == 'timeout'), 2] = 999999999
    #data = np.delete(data, timeout_rows, axis=0)
    print(data)
    nodes = data[1:, 0].astype(np.int32)
    probs = data[1:, 1].astype(np.int32)
    times = data[1:, 2].astype(np.float32)

    plt.figure()
    for p in np.unique(probs):
        current_nodes = nodes[probs == p]
        current_times = times[probs == p]

        plt.plot(current_nodes,
                 current_times,
                 label=f'p={p/100}',
                 marker='+',
                 ms=6)  #, s=20, marker='x')
    plt.legend(loc='upper left')
    #plt.yscale('log')
    plt.ylim([-10, 100])
    plt.title(f'Runtime of {args.system} system')
    plt.xlabel('Number of nodes')
    plt.ylabel('Time(s)')
    plt.savefig(args.outfile, dpi=600)