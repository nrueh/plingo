import argparse

parser = argparse.ArgumentParser(description='Generate plog2.0 grid instance.')
parser.add_argument('--m', type=int, help='width of grid')
parser.add_argument('--n', type=int, help='height of grid')

args = parser.parse_args()

if __name__ == '__main__':
    with open('base_encoding.plog', 'r') as f:
        encoding = f.read()
    encoding = encoding.replace('$M', str(args.m))
    encoding = encoding.replace('$N', str(args.n))
    leftof = [
        f'leftof(node({i},{j}),node({i+1},{j})).' for i in range(1, args.m)
        for j in range(1, args.n + 1)
    ]
    belowof = [
        f'belowof(node({i},{j}),node({i},{j+1})).'
        for i in range(1, args.m + 1) for j in range(1, args.n)
    ]
    encoding = encoding.replace('$LEFTOF', '\n'.join(leftof))
    encoding = encoding.replace('$BELOWOF', '\n'.join(belowof))

    with open(f'grid_{args.m}_{args.n}.plog', 'w') as f:
        f.write(encoding)
