'''
Used to convert original benchmark instances from Joohyung Lee to plingo format.
Including fixing some formatting errors, etc.
'''
import os

instance_dir = 'original_instances'
az_instances = os.listdir(instance_dir)

for i in az_instances:
    print(i)
    instance_path = os.path.join(instance_dir, i)
    with open(instance_path, 'r') as fp:
        lines = fp.readlines()
    new_program = []
    for l in lines:
        l = l.strip()
        if l == '' or l[0] == '%':
            continue
        if l[0] == 'p':
            # new_program.append(l)
            continue
        if 'go_go:' in l:
            l = l.replace('go_go:', 'go_go_')
        if i == '5646n64579e.txt':
            if l.startswith('query'):
                continue
            weight = l.split('::')[0]
            atom = l.split('::')[1]
            atom = atom.replace('\'', '\"')
        else:
            weight = l.split('  ')[0]
            atom = l.split('  ')[1]
        if atom[-1] == '.':
            atom = atom[:-1]
        if '/' in atom:
            atom = atom.replace('/', '_')
        new_line = f'{atom} :- &problog(\"{weight}\").'
        new_program.append(new_line)
    outpath = os.path.join('converted_instances', i.replace('.txt', '.lp'))
    new_program = '\n'.join(new_program)
    with open(outpath, 'w') as fp:
        fp.write(new_program)
