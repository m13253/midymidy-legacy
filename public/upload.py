#!/usr/bin/env python3

import cgi
import os
import sqlite3
import json
import time

import config
from misc import *
import music

def main():
    req=cgi.FieldStorage()
    if 'upload_file' in req:
        return process_upload(req)

    prbin('Status: 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n');

    prfile(privfile('htmlhead.html'))

    prbin(
'''<title>上传 - MidyMidy</title>
''')

    prfile(privfile('banner.html'))

    prbin(
'''<h1>上传</h1>
<hr />
<form id="upload_form" name="upload_form" action="upload.py" method="post" enctype="multipart/form-data">
<table><tbody>
<tr><td>文件：</td><td><input id="upload_file" name="upload_file" type="file" /></td></tr>
<tr><td>标题：</td><td><input id="upload_title" name="upload_title" /></td></tr>
<tr><td>简介：</td><td><textarea id="upload_desc" name="upload_desc"></textarea></td></tr>
<tr><td></td><td><input type="submit" /></td></tr>
</tbody></table>
</form>
''')

    prfile(privfile('htmlfoot.html'))

def process_upload(req):
    prbin('Status: 200 OK\r\nContent-Type: text/plain; charse=utf-8\r\n\r\n')
    prbin('Uploaded file detected!\n')
    if 'upload_file' in req:
        filename=req['upload_file'].filename
        prbin('Filename:\t%s\n' % filename)
        if filename.endswith('.mid'):
            filename=filename[:-4]
    else:
        filename=None
    if 'upload_title' in req:
        title=req['upload_title'].value
        prbin('Title:\t%s\n' % title)
    else:
        title=None
    if 'upload_desc' in req:
        desc=req['upload_desc'].value
        prbin('Description:\n%s\n' % desc)
    else:
        desc=None
    prbin('Updating database...\n')
    db=sqlite3.connect(datafile('midymidy.db'))
    mdid=music.addmusic(db, title, desc, filename, 0)
    prbin('Updated, ID=%s\n' % mdid)

if __name__=='__main__':
    runmain(main)

