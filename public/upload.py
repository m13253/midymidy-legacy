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
        prbin('Filename:\t%s\n' % req['upload_file'].filename)
    if 'upload_title' in req:
        prbin('Title:\t%s\n' % req['upload_title'].value)
    if 'upload_desc' in req:
        prbin('Description:\n%s\n' % req['upload_desc'].value)

if __name__=='__main__':
    runmain(main)

