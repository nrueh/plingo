import os

if __name__ == '__main__':
    logdir = 'logs'
    logs = os.listdir(logdir)
    logs.sort(reverse=True)
    print(logs)
    times = []

    for p in [100, 90, 80, 50]:
        for N in [5, 10, 20, 50, 100, 200, 500, 1000]:
            logfile = f'N{N}_p{p}.log'

            with open(os.path.join(logdir, logfile), 'r') as fp:
                data = fp.readlines()

            for line in data:
                if line.find('Time') == 0:
                    t = line[15:line.find('s')]

            times.append(f'N: {N}, p:{p}, Time: {t}')

    output = '\n'.join(times)
    with open('times.txt', 'w') as fp:
        fp.write(output)