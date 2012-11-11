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

def getmusicdata(musicid, columns):
    db=getdb('music.db')
    dbc=db.cursor()
    dbc.execute(sqlconv.col2select(columns, 'music', 'WHERE id=?'), (mdid.md2int(musicid),))
    musicdata=dbc.fetchone()
    if musicdata:
        return sqlconv.res2dict(columns, musicdata)
    else:
        return None

def addmusic(title, desc, filename, uploader):
    db=getdb('music.db')
    dbc=db.cursor()
    current_time=time.time()
    dbc.execute(sqlconv.col2insert(('title', 'desc', 'filename', 'ctime', 'mtime', 'uploader'), 'music'), (title, desc, filename, current_time, current_time, uploader))
    db.commit()
    dbc.execute('SELECT last_insert_rowid();')
    return dbc.fetchone()[0]

