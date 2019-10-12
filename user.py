from pymongo import MongoClient

_authorized_uids = list()
_user_states = dict()

class UserState():
    def __init__(self):
        self.params = UserState.defparams
        self.doing_task = False
        self.cur_task = None
    
    def new_task(self, t):
        self.doing_task = True
        self.current_task = t
    
    def finish_task(self):
        self.doing_task = False

def is_authorized(u):
    return u.id in _authorized_uids

def new(u):
    d = di(u)
    d['authorized'] = False
    db.insert_one(d)
    return u

def authorize(u):
    if not is_authorized(u):
        _authorized_uids.append(u.id)
        _user_states[u.id] = UserState()
        d = di(u)
        d['authorized'] = True
        db.update_one(find_id(u), {'$set': d})

def state(u):
    return _user_states[u.id]

def get_id_via_mention(ment):
    un = ment.lstrip('@')
    u = db.find_one({'username': un})
    if u: return u['id']

db = None

di = lambda u: {'id': u.id, 'name': u.first_name, 'username': u.username}
name = lambda u: u.first_name
find_id = lambda u: {'id': u.id}

def load_db(projname):
    cl = MongoClient()
    global db
    db = cl[projname].users
    for u in db.find():
        if u['authorized']:
            _authorized_uids.append(u['id'])
            _user_states[u['id']] = UserState()
