import argparse
import json

import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='Plot benchmark results.')
parser.add_argument('--our_file',
                    type=str,
                    help='CSV file containing our benchmark results')
parser.add_argument('--outfile', '-o', type=str, help='Path to save plot')
parser.add_argument('--az_file',
                    type=str,
                    help="CSV file containing azreasoners benchmark results")
args = parser.parse_args()

if __name__ == '__main__':
    our_data = np.genfromtxt(args.our_file,
                             delimiter=" ",
                             dtype=None,
                             encoding=None)
    our_nodes = our_data[1:, 0].astype(np.int32)
    our_times = our_data[1:, 1].astype(np.float32)

    az_data = np.genfromtxt(args.az_file,
                            delimiter=" ",
                            dtype=None,
                            encoding=None)
    az_nodes = az_data[1:, 0].astype(np.int32)
    az_times = az_data[1:, 1].astype(np.float32)

    # our_nodes = our_nodes[our_probs == 100][:6]
    # our_times = our_times[our_probs == 100][:6]

    # az_nodes = az_nodes[az_probs == 100][:6]
    # az_times = az_times[az_probs == 100][:6]

    plt.figure()
    plt.plot(our_nodes, our_times, label='ours', marker='+',
             ms=6)  #, s=20, marker='x')
    plt.plot(az_nodes, az_times, label='azreasoners', marker='+',
             ms=6)  #, s=20, marker='x')
    plt.legend(loc='upper left')
    #plt.yscale('log')
    plt.ylim([-0.5, 500])
    plt.title(f'Comparison of runtimes for marginal probabilities')
    plt.xlabel('Number of edges')
    plt.ylabel('Time(s)')
    plt.savefig(args.outfile, dpi=600)