from calendar import c
import json
import os
import sys
from unittest import result

import matplotlib.pyplot as plt
import numpy as np


def parse_json(d):
    data = {}
    for i in range(2, 10):
        data[i] = []

    for i in range(36):
        current_entry = d[str(i)]
        m = int(current_entry['name'][0])
        # n = int(current_entry['name'][-1])
        runtime = float(current_entry['runtime'])
        timeout = current_entry['timeout']
        data[m].append(runtime)
        # query_prob = current_entry['query_prob']
    return data


if __name__ == '__main__':
    result_files = os.listdir('results')[:-1]
    systems = ['problog', 'plingo', 'plog2']

    data = {}
    for system in systems:
        filename = [
            filename for filename in result_files if system in filename
        ][0]
        with open(os.path.join('results', filename), 'r') as f:
            data[system] = json.load(f)
    plot_from = 28
    plot_until = 36

    width = 0.15
    colors = ['blue', 'orange', 'green']
    x_adjustment = [-1, 0.0, +1]
    x_axis = list(range(plot_from + 1, plot_until + 1))
    xtick_labels = [
        entry['name']
        for i, entry in enumerate(data[list(data.keys())[0]].values())
        if plot_from <= i < plot_until
    ]

    for idx, system in enumerate(systems):
        if 'plingo problog' in system:
            continue
        current_data = data[system]
        runtimes = [
            float(current_data[i]['runtime']) + 1e-1 for i in current_data
            if plot_from <= int(i) < plot_until
        ]
        timeouts = [
            int(current_data[i]['timeout']) for i in current_data
            if plot_from <= int(i) < plot_until
        ]
        plt.bar([x + (x_adjustment[idx] * width) for x in x_axis],
                runtimes,
                width,
                color=colors[idx],
                label=system,
                tick_label=xtick_labels)

    plt.axhline(1200, color='grey', linestyle='dashdot', lw=0.5)
    plt.legend(loc='upper left')
    plt.yscale('log')

    plt.savefig('grid9.jpg', dpi=300)
