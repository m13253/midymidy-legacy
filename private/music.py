#!/usr/bin/env python3

import time

mdchars='23456789abcdefghjkmnpqstuvwxyz2'

def nextmusic(current):
    current=current.lower()
    if current.startswith('md'):
        current=current[2:]
    current=list(current)
    for i in current:
        if i not in mdchars:
            raise ValueError
    for i in range(len(current)-1, -1, -1):
        current[i]=mdchars[mdchars.find(current[i])+1]
        if current[i]!=mdchars[0]:
            return 'md'+''.join(current)
    return 'md'+mdchars[0]+''.join(current)

def getmusicdata(db, musicid):
    dbc=db.cursor()
    dbc.execute('SELECT id, title, desc, filename, time, uploader FROM music WHERE id=?;', (musicid,))
    musicdata=dbc.fetchone()
    if musicdata:
        return dict(zip(('id', 'title', 'desc', 'filename', 'time', 'uploader'), musicdata))
    else:
        return None

def addmusic(db, title, desc, filename, uploader):
    db.create_function('next_music', 1, nextmusic)
    dbc=db.cursor()
    dbc.execute('SELECT count(*) FROM music;')
    music_count=dbc.fetchone()[0]
    args=(title, desc, filename, time.time(), uploader)
    if music_count>0:
        dbc.execute('INSERT INTO music (id, title, desc, filename, time, uploader) VALUES (next_music((SELECT id FROM music WHERE no=(SELECT max(no) FROM music))), ?, ?, ?, ?, ?);', args)
    else:
        dbc.execute("INSERT INTO music (id, title, desc, filename, time, uploader) VALUES ('md2', ?, ?, ?, ?, ?);", args)
    db.commit()
    dbc.execute('SELECT last_insert_rowid();')
    lastid=dbc.fetchone()[0]
    dbc.execute('SELECT id FROM music WHERE no=?', (lastid,))
    return dbc.fetchone()[0]

