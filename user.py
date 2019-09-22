from pymongo import MongoClient

db = None

di = lambda u: {'id': u.id, 'name': u.first_name, 'username': u.username}
name = lambda u: u.first_name
find_id = lambda u: {'id': u.id}

def load_db(projname):
    cl = MongoClient()
    global db
    db = cl[projname]['users']

def update(u):
    db.update_one(find_id(u), {'$set': di(u)})

def check(u):
    t = db.find_one(find_id(u))
    return bool(t)

def register(u):
    db.insert_one(di(u))

