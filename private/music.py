#!/usr/bin/env python3

import time

mdchars='23456789abcdefghjkmnpqstuvwxyz'

def md2int(md):
    if md.startswith('md'):
        md=md[2:]
    res=0
    for i in md:
        if i not in mdchars:
            raise ValueError("invalid id: %s" % repr(md))
        res*=len(mdchars)
        res+=mdchars.find(i)+1
    return res

def int2md(no):
    if no<=0:
        raise ValueError("invalid id: %s" % repr(no))
    res=''
    while no>0:
        no, reminder=divmod(no-1, len(mdchars))
        res=mdchars[reminder]+res
    return "md"+res

def getmusicdata(db, musicid):
    dbc=db.cursor()
    dbc.execute('SELECT title, desc, filename, time, uploader FROM music WHERE id=?;', (musicid,))
    musicdata=dbc.fetchone()
    if musicdata:
        return dict(zip(('title', 'desc', 'filename', 'time', 'uploader'), musicdata))
    else:
        return None

def addmusic(db, title, desc, filename, uploader):
    dbc=db.cursor()
    dbc.execute("INSERT INTO music (title, desc, filename, time, uploader) VALUES (?, ?, ?, ?, ?);", (title, desc, filename, time.time(), uploader))
    db.commit()
    dbc.execute('SELECT last_insert_rowid();')
    return dbc.fetchone()[0]

