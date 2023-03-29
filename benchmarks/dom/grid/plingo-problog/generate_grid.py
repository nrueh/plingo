# import argparse

# parser = argparse.ArgumentParser(description='Generate problog grid instance.')
# parser.add_argument('--m', type=int, help='width of grid')
# parser.add_argument('--n', type=int, help='height of grid')

# args = parser.parse_args()


if __name__ == '__main__':
    for m in range(2,10):
        for n in range(2,m+1):
            with open('base_encoding.pl', 'r') as f:
                encoding = f.read()
            encoding = encoding.replace('$M', str(m))
            encoding = encoding.replace('$N', str(n))
            nodes = [
                f'node(({i},{j})).' for i in range(1, m + 1)
                for j in range(1, n + 1)
            ]
            encoding = encoding.replace('$INSTANCE', '\n'.join(nodes))

            with open(f'grid_{m}_{n}.pl', 'w') as f:
                f.write(encoding)   
