import argparse
import json
import os

parser = argparse.ArgumentParser(description='Parse results.')
parser.add_argument('--log', '-l', type=str, help='logfile containing results')

args = parser.parse_args()


def parse_plingo(instance):
    try:
        time_line = [line for line in instance if line.startswith('Time')][0]
    except IndexError:
        time_line = [line for line in instance if 'Time' in line][0]
    runtime = time_line.split(' : ')[1].split('(')[0].strip()[:-1]
    query_line = [line for line in instance if line.startswith('flow')][0]
    query_prob = query_line.split(':')[1].strip()
    return runtime, query_prob


def parse_plog(instance):
    runtime = instance[3].split('user')[0]
    query_line = instance[2]
    query_prob = query_line.split(':')[1].strip()
    return runtime, query_prob


def parse_problog(instance):
    runtime = instance[6].split(':')[1].strip()[:-1]
    query_prob = instance[7].split(':')[1].strip()
    return runtime, query_prob


if __name__ == '__main__':
    with open(args.log, 'r') as f:
        log = f.read().strip().split('START INSTANCE')[1:]
    results = {}
    mode = args.log.split('_')[1]

    for id_, instance in enumerate(log):
        results[id_] = {}
        lines = instance.strip().strip('\n').split('\n')
        current_instance = lines[0]
        results[id_]['name'] = current_instance
        if mode == 'plingo':
            if 'EXIT CODE 30' in instance or 'EXIT CODE 10' in instance:
                timeout = 0
                runtime, query_prob = parse_plingo(lines)
            elif 'EXIT CODE 137' in instance or 'TIME LIMIT' in instance:
                timeout = 1
                runtime = 1200
                try:
                    _, query_prob = parse_plingo(lines)
                except IndexError:
                    query_prob = None
            else:
                raise ValueError(f'Unknown exit code {instance}.')
        elif mode == 'plog2':
            if 'EXIT CODE 0' in instance:
                timeout = 0
                runtime, query_prob = parse_plog(lines)
            elif 'EXIT CODE 124' in instance or 'EXIT CODE 33' in instance:
                timeout = 1
                runtime = 1200
                query_prob = None
            else:
                raise ValueError(f'Unknown exit code {instance}.')
        elif mode == 'problog':
            if 'Timeout' in instance:
                timeout = 1
                runtime = 1200
                query_prob = None
            else:
                timeout = 0
                runtime, query_prob = parse_problog(lines)

        results[id_] = {
            'name': current_instance,
            'timeout': timeout,
            'runtime': runtime,
            'query_prob': query_prob
        }

    outname = os.path.basename(args.log).replace('.log', '.json')
    print(outname)
    with open(os.path.join('results', outname), 'w') as f:
        f.write(json.dumps(results))
