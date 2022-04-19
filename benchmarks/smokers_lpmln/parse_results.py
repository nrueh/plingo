import argparse
import json
import os

parser = argparse.ArgumentParser(description='Parse results.')
parser.add_argument('--log', '-l', type=str, help='logfile containing results')
parser.add_argument('--out',
                    '-o',
                    type=str,
                    default=None,
                    help='Suffix for output result file')

args = parser.parse_args()


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
    mode = os.path.basename(args.log).split('_')[1]

    for id_, instance in enumerate(log):
        results[id_] = {}
        lines = instance.strip().strip('\n').split('\n')
        current_instance = lines[0]
        if mode == 'plingo':
            if 'EXIT CODE 30' in instance:
                timeout = 0
                time_line = [
                    line for line in lines if line.startswith('Time')
                ][0]
                runtime = time_line.split(' : ')[1].split('(')[0].strip()[:-1]
            elif 'EXIT CODE 11' in instance:
                timeout = 1
                runtime = 1200
            else:
                raise ValueError(f'Unknown exit code {instance}.')
        elif mode == 'lpmln':
            if 'EXIT CODE 0' in instance:
                timeout = 0
                time_line = [
                    line for line in lines if line.startswith('Total time:')
                ][0]
                runtime = time_line.split(': ')[1].split('(')[0].strip()[:-1]
            elif 'EXIT CODE 124' in instance or 'EXIT CODE 33' in instance:
                timeout = 1
                runtime = 1200
            else:
                raise ValueError(f'Unknown exit code {instance}.')
        # elif mode == 'problog':
        #     if 'Timeout' in instance:
        #         timeout = 1
        #         runtime = 1200
        #         query_prob = None
        #     else:
        #         timeout = 0
        #         runtime, query_prob = parse_problog(lines)

        results[id_] = {
            'name': current_instance,
            'timeout': timeout,
            'runtime': runtime
        }

    outname = os.path.basename(args.log).replace('.log', '')
    if args.out is not None:
        outname = outname + '_' + args.log
    outname = outname + '.json'
    print(outname)
    with open(os.path.join('results', outname), 'w') as f:
        f.write(json.dumps(results))
