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

    prbin('Status: 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n');

    prfile(privfile('htmlhead.html'))

    prbin(
'''<title>最新上传 - MidyMidy</title>
''')

    prfile(privfile('banner.html'))

    prbin(
'''<h1>最新上传</h1>
<hr />
<table width="100%"><tbody>
<tr><th>ID</th><th width="*">标题</th><th>时间</th></tr>
''')
    for i in dbman.getmusiclist(('id', 'title', 'ctime'), 'ORDER BY ctime DESC'):
        prbin('<tr><td>%s</td><td><a href="play.py?id=%s">%s</a></td><td style="text-align: right">%s</td></tr>\n' % (escape_for_html(mdid.int2md(i['id'])), escape_for_prop(mdid.int2md(i['id'])), escape_for_html(i['title']), escape_for_html(time.strftime("%c", time.localtime(i['ctime'])))))
    prbin(
'''</tbody></table>
''')

    prfile(privfile('htmlfoot.html'))

if __name__=='__main__':
    runmain(main)

