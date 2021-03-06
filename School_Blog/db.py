import sqlite3
from datetime import datetime as dt
import hashlib

def get_conn(self=None):
    conn = sqlite3.connect('database.db')
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    if self:
        self.conn = conn
        self.cur = cur
    else:
        return (conn, cur)

class Log:
    def __init__(self, message, title, image, topic, id=None, date=None):
        if isinstance(message, list):
            self.text = message
        else:
            self.text = [message,]
        self.title = title
        self.image = image
        self.topic = topic
        self.date = date
        self.id = id

        get_conn(self)

    def __str__(self):
        return '\n'.join(self.text)

    def add(self):
        '''
        Add the log to the 'posts' table
        '''
        if self.date == None:
            self.date = dt.now()
        self.cur.execute('''INSERT INTO posts (topicid, title, message, created, image) VALUES (?, ?, ?, ?, ?)''',
                                            (self.topic, self.title, str(self.text), self.date, self.image))
        self.conn.commit()
        self.id = self.cur.lastrowid

    def save(self):
        '''
        Update the modified data in the 'posts' table
        '''
        self.date = dt.now()
        self.cur.execute('''UPDATE posts SET created = ?, title = ? WHERE id = ?''', (self.date, self.title, self.id))
        self.conn.commit()

    @staticmethod
    def get(id):
        '''
        Return a post based on the id of it.
        '''
        conn, cur = get_conn()

        cur.execute('''SELECT * FROM posts WHERE id = ?''', (id,))
        row = cur.fetchone()
        if row:
            id, uid, title, mess, date, image = row
            print(uid)
            return Log(eval(mess), title, image, uid, id, date)
        return None

    @staticmethod
    def delete(id):
        '''
        Delete a post with a given id
        '''
        conn, cur = get_conn()

        cur.execute('''DELETE FROM posts WHERE id = ?''', (id, ))
        conn.commit()

    @staticmethod
    def get_newest(tid):
        '''
        Get the newest post for a given topic
        '''
        conn, cur = get_conn()

        cur.execute('''SELECT * FROM posts WHERE topicid = ? ORDER BY created DESC''', (tid,))
        row = cur.fetchone()
        if row:
            id, tid, title, message, created, image = row
            return Log(eval(message), title, image, tid, id, created)

    @staticmethod
    def get_all(tid):
        '''
        Get all the posts for a given topic
        '''
        conn, cur = get_conn()

        logs = []
        cur.execute('''SELECT * FROM posts WHERE topicid = ? ORDER BY created DESC''', (tid,))
        for row in cur:
            id, tid, title, message, created, image = row
            logs.append( Log(eval(message), title, image, tid, id, created) )
        return logs

    def get_topic(self):
        '''
        Get the topic of the current post
        '''
        return Topic.get(self.topic)

class Comment:
    pass

class Topic:
    def __init__(self, title, subtitle, date=None, id=None, post=None):
        self.title = title
        self.subtitle = subtitle
        if date:
            self.date = date
        if id:
            self.id = id
        if post:
            self.post = post

        get_conn(self)

    def add(self):
        '''
        Add the topic to the 'topics' table
        '''
        date = dt.now()
        self.cur.execute('''INSERT INTO topics (title, subtitle, created) VALUES (?, ?, ?)''',
                                            (self.title, self.subtitle, date))
        self.conn.commit()
        self.id = self.cur.lastrowid
        self.date = date

    def save(self):
        '''
        Update the modified data in the 'topics' table
        '''
        self.date = dt.now()
        self.cur.execute('''UPDATE topics SET created = ?, title = ?, subtitle = ? WHERE id = ?''',
                    (self.date, self.title, self.subtitle, self.id))
        self.conn.commit()

    @staticmethod
    def get(id):
        '''
        Return a topic based on the id of it.
        '''
        conn, cur = get_conn()

        cur.execute('''SELECT * FROM topics WHERE id = ? ORDER BY created ASC''', (id,))
        row = cur.fetchone()
        if row:
            id, title, subtitle, date = row
            return Topic(title, subtitle, date, id)
        return None

    @staticmethod
    def get_main_page():
        conn, cur = get_conn()

        cur.execute('''SELECT * FROM topics ORDER BY created DESC''')
        topics = []
        i = 0
        for row in cur:
            # print(row)
            if i == 3:
                break
            id, title, sub, date = row
            topics.append(Topic(title, sub, date, id))
            i += 1
        for i in range(len(topics)):
            post = Log.get_newest(topics[i].id)
            topics[i].post = post
        topics.reverse()
        return topics


if __name__ == "__main__":
#    t = Log.delete(35)
#   t = Topic("Topic 2 - IPT", "Vector Graphics System")
#   t.add()
#   print("Topic Added to database")
   pass
    # Add adjustments to anything here!
