import sys
import sqlite3
from datetime import datetime as dt

conn = sqlite3.connect('database.db')
conn.execute("PRAGMA foreign_keys = ON")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

log_file = sys.argv[1]

logs = open(log_file).read().split('...')

for log in logs:
    dc = {}
    for line in log.split('\n'):
        line = line.split('|')
        if line != ['']:
            print(line)
            dc[line[0]] = '|'.join(line[1:])

    cur.execute('''INSERT INTO posts (topicid, title, message, created, image) VALUES (?, ?, ?, ?, ?)''',
                                        (int(dc.get('topic')), dc.get('title'), str(dc.get('text')), dc.get('date'), dc.get('image')))
    conn.commit()
