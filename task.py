from ling import filter_words_starts_with, word_in, neg_word_in, ru_week_days

tasklist = list()
# when we need to load task from org file

def new(u, m):
    return Task(user=u, tc=m.date)

class Task:
    def __init__(self, user=None, tc=None):
        self.author = user
        self.time_created = tc 
        self.description = str()
        self.story = list()
        self.story_time = list()
        self.text_priority = str()
        self.priority = -1
        self.hashtags = list()
        self.mentions = list()
        self.deadline = None
        self.subscribers = [self.author]
        self.participants = []
        self.potential_participants = []
        self.declined = []
        tasklist.append(self)
    
    def _parse_text(self, txt):
        self.hashtags += filter_words_starts_with('#', txt)
        self.mentions += filter_words_starts_with('@', txt)
        ...
        
    def add_description(self, txt):
        self._parse_text(txt)
        self.description = txt
    
    def set_priority(self, txt):
        self.text_priority = txt
        if neg_word_in('важно', t):
            self.priority = 0
        elif word_in('желательно', t) or word_in('возможно', t):
            self.priority = 1
        elif word_in('важно', t) or word_in('срочно', t):
            self.priority = 2
        else:
            self.priority = 1
    
    def is_taken(self):
        return bool(self.participants)
