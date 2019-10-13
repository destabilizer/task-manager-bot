from pathlib import Path

up = Path('users')
ap = Path('admins')

if not up.exists(): up.touch()
if not ap.exists(): ap.touch()

u = list(map(lambda s: s.rstrip('\n ').split('\t'), open(up).readlines()))
a = list(map(lambda s: s.rstrip('\n '), open(ap).readlines()))

writerow = lambda f, r: f.write('\t'.join(r)+'\n')

def insert_user(r):
    with open(up, 'a') as uf:
        writerow(uf, r)
    u.append(r)

def delete_user(r):
    with open(up, 'w') as uf:
        for i in u:
            if i[0] == r[0]:
                u.remove(i)
            else:
                writerow(uf, i)

def is_user(r):
    return r[0] in map(lambda t: t[0], u)

def is_admin(r):
    return r[0] in a

def find_by_username(un):
    for i in u:
        if i[2] == un: return i

def update_user(r):
    for i in u:
        if i[0] == r[0] and i != r:
            delete_user(r)
            insert_user(r)
