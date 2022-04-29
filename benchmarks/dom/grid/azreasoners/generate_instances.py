if __name__ == '__main__':
    for m in range(2, 10):
        for n in range(2, m + 1):
            encoding = f'm({m}). n({n}).'

            with open(f'instances/grid_{m}_{n}.lp', 'w') as f:
                f.write(encoding)
