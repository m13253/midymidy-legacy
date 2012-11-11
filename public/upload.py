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

def main():
    if detect_ie():
        exit()

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
<tr><td></td><td><input type="submit" value="上传" /></td></tr>
</tbody></table>
</form>
''')

    prfile(privfile('htmlfoot.html'))

def process_upload(req):
    if 'upload_file' in req:
        uploadfile=req['upload_file'].file
        if not uploadfile:
            error_page('403 Forbidden', '您的文件不符合要求。')
            exit()
    else:
        error_page('403 Forbidden', '您的文件不符合要求。')
        exit()

    filename=str(uuid.uuid4())
    buf=uploadfile.read(4194305)
    if len(buf)>4194304:
        error_page('403 Forbidden', '您的文件大小超过了&nbsp;4MB。')
        exit()
    with open("midi/pending/%s.mid" % filename, "wb") as f:
        f.write(buf[:4194304])
    del buf
    try:
        os.chmod("midi/pending/%s.mid" % filename, 0o666)
    except:
        pass

    if 'upload_title' in req:
        title=req['upload_title'].value
    else:
        title=''
    if 'upload_desc' in req:
        desc=req['upload_desc'].value
    else:
        desc=''

    db=sqlite3.connect(datafile('midymidy.db'))
    dbman.addmusic(title, desc, filename, 0)
    prbin('Status: 302 Found\r\nLocation: pending.py\r\n\r\n')

if __name__=='__main__':
    runmain(main)

