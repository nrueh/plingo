import os

instance_dir = 'az_instances/lpmln2asp-input'
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
            new_program.append(l)
            continue
        if i == '5646n64579e.txt':
            weight = l.split('::')[0]
            atom = l.split('::')[1]
        else:
            weight = l.split('  ')[0]
            atom = l.split('  ')[1]

        new_line = f'{atom} :- &problog(\"{weight}\").'
        new_program.append(new_line)
    outpath = os.path.join('instances', i.replace('.txt', '.lp'))
    new_program = '\n'.join(new_program)
    with open(outpath, 'w') as fp:
        fp.write(new_program)