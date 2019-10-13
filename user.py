import userlist

users = list()

from task import Task

def wrap(func):
    return lambda msg: func(User(msg.from_user), msg)

class User:
    def __new__(cls, tguser=None):
        # if already exists
        if tguser:
            for u in users:
                if u.id == tguser.id:
                    u._update_tguser(tguser)
                    return u
        # otherwise create
        u = super(User, cls).__new__(cls)
        users.append(u)
        return u
    
    def __init__(self, tguser=None):
        self.tguser = tguser
        self.id = None
        self.name = None
        self.un = None
        self.authorized = False
        self.isadmin = False
        self.state = UserState()
        self.created_tasks = list()
        if tguser: self._update_tguser(tguser)
    
    @classmethod
    def via_mention(cls, mention):
        un = mention.lstrip('@')
        for u in users:
            if u.un == un:
                return u
        else:
            u = super(User, cls).__new__(cls)
            u.un = un
            r = userlist.find_by_username(un)
            if r: self.restore(r)
            return u
    
    def _update_tguser(self, tguser):
        self.tguser = tguser
        self.id = tguser.id
        self.name = tguser.first_name
        self.un = tguser.username
        self.authorized = userlist.is_user(self.r())
        userlist.update_user(self.r())
    
    def r(self):
        return [str(self.id), str(self.name), str(self.un)]

    def register(self):
        userlist.insert_user(self.r())
        self.authorized = True
    
    def ban(self):
        userlist.delete_user(self.r())
        self.authorized = False
    
    def restore(self, r):
        self.id = r[0]
        self.name = r[1]
        self.un = r[2]
        self.authorized = True
        self.isadmin = userlist.is_admin(r)
    
    def __repr__(self):
        return ' '.join(self.r())
    
    def create_task(self, m):
        t = Task(user=self, tc=m.)
        self.state.new_task(t)
        self.created_tasks.append(t)
        return t
    
    def current_task(self):
        return self.state.cur_task
    
    def finish_creating_task(self):
        self.state.finish_task()
        

via_mention = User.via_mention

class UserState():
    def __init__(self):
        self.creating_task = False
        self.cur_task = None
    
    def new_task(self, t):
        self.creating_task = True
        self.current_task = t
    
    def finish_task(self):
        self.creating_task = False


for r in userlist.u:
    u = User()
    u.restore(r)
