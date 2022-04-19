import argparse
from os import rename

parser = argparse.ArgumentParser(description='Get Nodes and Edges.')
parser.add_argument('--instance', '-i', type=str, help='input file')

args = parser.parse_args()

if __name__ == '__main__':
    with open(args.instance, 'r') as f:
        lines = f.read().strip().split('\n')
    nodes = []
    for edge in lines:
        edge = edge.split(':-')[0]
        edge = edge.strip()
        two_nodes = edge[edge.index('(') + 1:edge.index(')')].split(',')
        for n in two_nodes:
            if n not in nodes:
                nodes.append(n)

    nodes = len(nodes)
    edges = len(lines)

    print("nodes")
    print(nodes)
    print("edges")
    print(edges)
    rename(args.instance, f'{nodes}n{edges}e.lp')
