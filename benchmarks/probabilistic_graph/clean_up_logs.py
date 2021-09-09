import os

logdir = 'logs'
logs = os.listdir(logdir)

for log in logs:
    logpath = os.path.join(logdir, log)
    with open(logpath, 'r') as fp:
        lines = fp.readlines()
    clean_log = []
    for line in lines:
        if 'Probability' not in line:
            clean_log.append(line)
    clean_log = ''.join(clean_log)
    with open(logpath, 'w') as fp:
        fp.write(clean_log)