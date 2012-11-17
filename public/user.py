#!/usr/bin/env python3

import cgi
import sqlite3

import config
from misc import *
import dbman

def main():
    if detect_ie():
        exit()

    req=cgi.FieldStorage()
    if 'action' not in req:
        prbin('Status: 405 Method Not Allowed\r\n\r\n')
    elif req['action'].value=='register':
        return user_register(req)
    elif req['action'].value=='login':
        return user_login(req)
    else:
        prbin('Status: 405 Method Not Allowed\r\n\r\n')

def user_register(req):
    if 'reg_action' in req:
        prbin('Status: 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n')
        exit()
    prbin('Status: 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n')
    prfile(privfile('htmlhead.html'))
    prbin('<title>注册 - MidyMidy</title>\n')
    prfile(privfile('banner.html'))

    prbin(
'''<h1>注册</h1>
<hr />
<form action="user.py" method="post">
<input type="hidden" id="action" name="action" value="register" />
<input type="hidden" id="reg_action" name="reg_action" value="register" />
<table><tbody>
<tr><td>邀请码：</td><td><input id="reg_invite" name="reg_invite" /></td>
<tr><td>邮箱：</td><td><input id="reg_email" name="reg_email" /></td>
<tr><td>密码：</td><td><input type="password" id="reg_passwd" name="reg_passwd" /></td>
<tr><td>确认密码：</td><td><input type="password" id="reg_passwd_again" /></td>
<tr><td>昵称：</td><td><input id="reg_nick" name="reg_nick" /></td>
<tr><td></td><td><input type="submit" value="注册" /></td></tr>
</tbody></table>
</form>
''')

    prfile(privfile('htmlfoot.html'))
    
def user_login(req):
    pass

if __name__=='__main__':
    runmain(main)

