import sqlite3
from datetime import datetime as dt
import hashlib

conn = sqlite3.connect('database.db')
conn.execute("PRAGMA foreign_keys = ON")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

class Log:
    def __init__(self, message, title, image, user, id=None, date=None):
        self.text = message
        self.title = title
        self.image = image
        self.user = user
        self.date = date
        self.id = id

    def add(self):
        '''
        Add the log to the 'posts' table
        '''
        date = datetime.now()
        cur.execute('''INSERT INTO posts (userid, title, message, created, image) VALUES (?, ?, ?, ?, ?)''',
                                            (self.user.id, self.title, self.text, date, self.image))
        conn.commit()
        self.id = cur.lastrowid
        self.date = date
        pass

    def save(self):
        '''
        Update the modified data in the 'posts' table
        '''
        self.date = datetime.now()
        cur.execute('''UPDATE posts SET created = ?, title = ? WHERE id = ?''', (self.date, self.title, self.id))
        conn.commit()

    @staticmethod
    def get(id):
        '''
        Return a post based on the id of it.
        '''
        cur.execute('''SELECT * FROM posts WHERE id = ?''', (self.id,))
        row = cur.fetchone()
        if row:
            id, uid, title, mess, date, image = row
            return Log(mess, title, image, uid, id, date)
        return None

class User:
    def __init__(self, username, passwd_hash, pcsave='', id=None):
        self.username = username
        self.password = passwd_hash
        self.save = pcsave
        self.id = id

    def add(self):
        '''
        Add a new user to the 'users' table in the database
        '''
        cur.execute("SELECT * FROM users WHERE username = ?", (self.username,))
        for row in cur:
            raise Exception("User {} already Exists!!!".format(self.username))
        cur.execute('''INSERT INTO users (username, password, pcsave) VALUES (?, ?, ?)''', (self.username, self.password, self.save))
        conn.commit()
        self.id = cur.lastrowid

    def save(self):
        '''
        Update the data in the 'users' table in the database
        '''
        cur.execute('''
                    UPDATE users
                    SET password = ?, pcsave = ?
                    WHERE id = ?
                    ''', (self.password, self.save, self.id))
        conn.commit()

    @staticmethod
    def get(id=None, uname=''):
        '''
        Get a User object from the 'users' table by id or username
        '''
        if id:
            cur.execute('''SELECT * FROM users WHERE id = ?''', (id,))
        elif uname:
            cur.execute('''SELECT * FROM users WHERE username = ?''', (uname,))
        row = cur.fetchone()
        if row is not None:
            id, uname, passwd, save = row
            return User(uname, passwd, save, id)
        return None
