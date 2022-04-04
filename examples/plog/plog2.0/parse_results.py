import argparse
import json
import os

parser = argparse.ArgumentParser(description='Parse results.')
parser.add_argument('--log', '-l', type=str, help='logfile containing results')

args = parser.parse_args()


def parse_plingo(instance):
    time_line = [line for line in instance if line.startswith('Time')][0]
    runtime = time_line.split(' : ')[1].split('(')[0].strip()[:-1]
    query_line = [line for line in instance if line.startswith('flow')][0]
    query_prob = query_line.split(':')[1].strip()
    return runtime, query_prob


def parse_plog(instance):
    runtime = instance[3].split('user')[0]
    query_line = instance[2]
    query_prob = query_line.split(':')[1].strip()
    return runtime, query_prob


if __name__ == '__main__':
    with open(args.log, 'r') as f:
        log = f.read().strip().split('\n')
    results = {}

    idx = [i for i, line in enumerate(log) if ' x ' in line]
    idx.append(-1)
    instances = [log[idx[i]:idx[i + 1]] for i in range(len(idx) - 1)]

    for instance in instances:
        current_instance = instance[0].strip()
        results[current_instance] = {}
        if 'plingo' in instance[1]:
            if 'OPTIMUM FOUND' in instance:
                results[current_instance]['timeout'] = 0
                runtime, query_prob = parse_plingo(instance)
            else:
                results[current_instance]['timeout'] = 1
                runtime = 1200
                query_prob = None
        elif 'Plog' in instance[1]:
            if 'Command exited with non-zero status 124' in instance:
                results[current_instance]['timeout'] = 1
                runtime = 1200
                query_prob = None
            else:
                results[current_instance]['timeout'] = 0
                runtime, query_prob = parse_plog(instance)

        results[current_instance]['runtime'] = runtime
        results[current_instance]['query_prob'] = query_prob

    outname = os.path.basename(args.log).replace('.log', '.json')
    with open(os.path.join('results', outname), 'w') as f:
        f.write(json.dumps(results))
