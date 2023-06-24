import datetime
# from fuzzywuzzy import fuzz
import hashlib
import config

from dataclasses import dataclass

@dataclass
class Submission:
    id: int
    title: str
    author: str
    text: str
    url: str
    url_hostname: str
    url_scheme: str
    submitted_by: str
    created_at: str
    title_md5: str
    text_md5: str
    title_len_ch: int
    text_len_ch: int
    title_len_words: int
    text_len_words: int

    def __init__(self, id, title, author, text, url, submitted_by, created_at = None):
        self.id = id
        self.title = title
        self.author = author
        self.text = text
        self.url = url
        self.submitted_by = submitted_by
        self.created_at = created_at or datetime.datetime.now(config.TIMEZONE).isoformat()
        self.title_md5 = hashlib.md5(title.encode('utf-8')).hexdigest()
        self.text_md5 = hashlib.md5(text.encode('utf-8')).hexdigest()
        self.title_len_ch = len(title)
        self.text_len_ch = len(text)
        self.title_len_words = len(title.split())
        self.text_len_words = len(text.split())
        self.url_hostname = url.split('/')[2]
        self.url_scheme = url.split('/')[0]
    
    def as_dict(self, full = False):
        if not full:
            return {
                "id": self.id,
                "title": self.title,
                "author": self.author,
                "text": self.text,
                "created_at": self.created_at
            }
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "text": self.text,
            "url_hostname": self.url_hostname,
            "url_scheme": self.url_scheme,
            "submitted_by": self.submitted_by,
            "created_at": self.created_at,
            "title_md5": self.title_md5,
            "text_md5": self.text_md5,
            "title_len_ch": self.title_len_ch,
            "text_len_ch": self.text_len_ch,
            "title_len_words": self.title_len_words,
            "text_len_words": self.text_len_words
        }
    
    def match(self, title = None, author = None):
        cond1, cond2 = True, True
        if title:
            # cond1 = fuzz.partial_ratio(title.lower(), self.title.lower()) > 80
            cond1 = title.lower() in self.title.lower()
        if author:
            cond2 = author.lower() in self.author.lower()
        return cond1 and cond2


class InMemoryDB:
    def __init__(self):
        self.submissions = []
        self.len = 0
        
    def add_submission(self, title, author, text, url, submitted_by, created_at = None):
        submission = Submission(self.len, title, author, text, url, submitted_by, created_at)
        self.submissions.insert(0, submission)
        self.len += 1
        return submission
    
    def search_submissions(self, title = None, author = None, size = 50):
        r = []
        ri = 0
        for s in self.submissions:
            if s.match(title, author):
                r.append(s)
                ri += 1
            if ri >= size:
                break
        return r
    
    def get_submission(self, id):
        if id >= self.len:
            return None
        return self.submissions[self.len - id - 1]
        
