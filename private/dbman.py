#!/usr/bin/env python3

import sqlite3
import time

import mdid
import misc
import sqlconv

dbs = {}

def getdb(name):
    if name not in dbs:
        dbs[name]=sqlite3.connect(misc.datafile(name))
    return dbs[name]

# music.db

def getmusicdata(musicid, columns):
    db=getdb('music.db')
    dbc=db.cursor()
    dbc.execute(sqlconv.col2select(columns, 'music', 'WHERE id=?'), (mdid.md2int(musicid),))
    musicdata=dbc.fetchone()
    if musicdata:
        return sqlconv.res2dict(columns, musicdata)
    else:
        return None

def getmusicdatabyfn(filename, columns):
    db=getdb('music.db')
    dbc=db.cursor()
    dbc.execute(sqlconv.col2select(columns, 'music', 'WHERE filename=?'), (mdid.md2int(filename),))
    musicdata=dbc.fetchone()
    if musicdata:
        return sqlconv.res2dict(columns, musicdata)
    else:
        return None

def getmusiclist(columns, conditions, condargs=()):
    db=getdb('music.db')
    dbc=db.cursor()
    dbc.execute(sqlconv.col2select(columns, 'music', conditions), condargs)
    while True:
        musicdata=dbc.fetchone()
        if musicdata:
            yield sqlconv.res2dict(columns, musicdata)
        else:
            break

def addmusic(title, desc, filename, uploader):
    db=getdb('music.db')
    dbc=db.cursor()
    current_time=time.time()
    dbc.execute(sqlconv.col2insert(('title', 'desc', 'filename', 'ctime', 'mtime', 'uploader'), 'music'), (title, desc, filename, current_time, current_time, uploader))
    db.commit()
    dbc.execute('SELECT last_insert_rowid();')
    return dbc.fetchone()[0]

# vote.db

def getplaycount(musicid):
    db=getdb('vote.db')
    dbc=db.cursor()
    dbc.execute('SELECT view FROM view WHERE id=?', (musicid,))
    res=dbc.fetchone()
    if res!=None:
        return res[0]
    else:
        return None


def incplaycount(musicid):
    db=getdb('vote.db')
    dbc=db.cursor()
    try:
        dbc.execute('INSERT INTO view (id, view) VALUES (?, 1)', (musicid,))
    except sqlite3.IntegrityError:
        dbc.execute('UPDATE view SET view=view+1 WHERE id=?', (musicid,))
    db.execute()
    dbc.execute('SELECT view FROM view WHERE id=?', (musicid,))
    return dbc.fetchone()[0]

