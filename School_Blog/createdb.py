import sqlite3
import datetime

open('database.db', 'w').close()

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''
  CREATE TABLE topics (
  	id INTEGER NOT NULL,
  	title TEXT NOT NULL,
  	subtitle TEXT NOT NULL,
    created TEXT NOT NULL,
  	PRIMARY KEY (id)
);
'''
)

cur.execute('''
  CREATE TABLE posts (
  	id INTEGER NOT NULL,
  	topicid INTEGER NOT NULL,
  	title TEXT NOT NULL,
    message TEXT NOT NULL,
    created TIMESTAMP NOT NULL,
    image TEXT NOT NULL,
  	PRIMARY KEY (id),
  	FOREIGN KEY (topicid) REFERENCES topics(id) ON DELETE CASCADE
);
'''
)

cur.execute('''
  CREATE TABLE comments (
    id INTEGER NOT NULL,
    postid INTEGER NOT NULL,
    comment TEXT NOT NULL,
    created TIMESTAMP NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (postid) REFERENCES posts(id) ON DELETE CASCADE
);
'''
)

conn.commit()
