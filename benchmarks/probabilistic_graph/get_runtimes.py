import os


def get_time_ours(log):
    time = ''
    logpath = os.path.join(logdir, log)
    with open(logpath, 'r') as fp:
        lines = fp.readlines()

    for line in lines:
        if line[:4] != 'Time':
            continue
        time = line.split(':')[1][1:]
        time = time[:time.find('s')]
    return time


def get_time_az(log):
    time = ''
    logpath = os.path.join(logdir, log)
    with open(logpath, 'r') as fp:
        lines = fp.readlines()
    if lines != []:
        time = lines[0].split(':')[1][2:-7]
    return time


if __name__ == '__main__':
    logtype = 'azreasoners'

    if logtype == 'ours':
        logdir = 'logs'
    elif logtype == 'azreasoners':
        logdir = 'logs_az'

    logs = os.listdir(logdir)
    logs.sort(key=lambda log: int(log[10:-4]))

    csv = []
    csv = ['N t']
    for log in logs:
        num_nodes = log[10:-4]

        if logtype == 'ours':
            time = get_time_ours(log)
        elif logtype == 'azreasoners':
            time = get_time_az(log)

        csv.append(f'{num_nodes} {time}')

    csv = '\n'.join(csv)
    with open(f'runtimes_{logtype}.csv', 'w') as fp:
        fp.write(csv)