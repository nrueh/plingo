from email.mime import base

if __name__ == '__main__':
    basepath = 'base_encoding.plog'
    with open(basepath, 'r') as f:
        base_encoding = f.read()

    max_days = 30
    for i in range(1, max_days + 1):
        new_encoding = base_encoding.replace('$DAYS', str(i))
        looks = [f'look({j})=p1.' for j in range(1, i + 1)]
        new_encoding = new_encoding.replace('$LOOKS', '\n'.join(looks))

        with open(f'squirrel{i}.plog', 'w') as f:
            f.write(new_encoding)
