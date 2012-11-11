#!/usr/bin/env python3

import cgi
import os
import sqlite3
import json
import time
import uuid

import config
from misc import *
import dbman
import mdid

def main():
    if detect_ie():
        exit()

    req=cgi.FieldStorage()
    db=sqlite3.connect(datafile('music.db'))
    dbc=db.cursor()

    prbin('Status: 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n');

    prfile(privfile('htmlhead.html'))

    prbin(
'''<title>正在处理 - MidyMidy</title>
<meta http-equiv="refresh" content="5" />
''')

    prfile(privfile('banner.html'))

    prbin(
'''<h1>正在处理</h1>
<hr />
<table width="100%"><tbody>
<tr><th>ID</th><th width="*">标题</th><th>时间</th><th>状态</th></tr>
''')
    dirlisting=os.listdir('midi/pending')
    for midifile in dirlisting:
        if midifile.endswith('.mid'):
            midifile=midifile[:-4]
            dbc.execute('SELECT id, title, mtime FROM music WHERE filename=?;', (midifile,))
            musicinfo=dbc.fetchone()
            if not musicinfo:
                continue
            prbin('<tr><td>%s</td><td>%s</td><td>%s</td><td>' % (escape_for_html(mdid.int2md(musicinfo[0])), escape_for_html(musicinfo[1]), escape_for_html(time.strftime("%c", time.localtime(musicinfo[2])))))
            if midifile+'.ogg' in dirlisting:
                prbin('正在转码</td></tr>\n')
            elif midifile+'.wav' in dirlisting:
                prbin('正在渲染</td></tr>\n')
            else:
                prbin('正在排队</td></tr>\n')
    prbin(
'''</tbody></table>
''')

    prfile(privfile('htmlfoot.html'))

if __name__=='__main__':
    runmain(main)

