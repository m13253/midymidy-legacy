#!/usr/bin/env python3

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
    return mdchars[0]+''.join(current)

def getmusicdata(db, musicid):
    dbc=db.cursor()
    dbc.execute('SELECT id, title, desc, filename, time, uploader FROM music WHERE id=?;', (musicid,))
    musicdata=dbc.fetchone()
    if musicdata:
        return dict(zip(('id', 'title', 'desc', 'filename', 'time', 'uploader'), musicdata))
    else:
        return None

