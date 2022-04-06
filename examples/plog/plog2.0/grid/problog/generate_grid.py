import argparse

parser = argparse.ArgumentParser(description='Generate problog grid instance.')
parser.add_argument('--m', type=int, help='width of grid')
parser.add_argument('--n', type=int, help='height of grid')

args = parser.parse_args()

if __name__ == '__main__':
    with open('base_encoding.pl', 'r') as f:
        encoding = f.read()
    encoding = encoding.replace('$M', str(args.m))
    encoding = encoding.replace('$N', str(args.n))
    nodes = [
        f'node(({i},{j})).' for i in range(1, args.m + 1)
        for j in range(1, args.n + 1)
    ]
    encoding = encoding.replace('$INSTANCE', '\n'.join(nodes))

    with open(f'grid_{args.m}_{args.n}.pl', 'w') as f:
        f.write(encoding)
