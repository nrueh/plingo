import argparse

parser = argparse.ArgumentParser(description='Generate plog2.0 grid instance.')
parser.add_argument('--m', type=int, help='width of grid')
parser.add_argument('--n', type=int, help='height of grid')

args = parser.parse_args()

if __name__ == '__main__':
    rightof = [
        f'rightof(({i},{j}),({i+1},{j})).' for i in range(1, args.m)
        for j in range(1, args.n + 1)
    ]
    belowof = [
        f'belowof(({i},{j}),({i},{j+1})).' for i in range(1, args.m + 1)
        for j in range(1, args.n)
    ]
    encoding = rightof + belowof

    with open(f'grid_{args.m}_{args.n}.lp', 'w') as f:
        f.write('\n'.join(encoding))
