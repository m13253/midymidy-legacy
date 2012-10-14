#!/usr/bin/env python3

import cgi
import os
import sqlite3

import config
import misc

req=cgi.FieldStorage()
if 'id' in req:
    db=sqlite3.connect(misc.datafile('midymidy.db'))
    dbc=db.cursor()
    dbc.execute('SELECT * FROM music WHERE id=?;', (req['id'],))
    musicdata=dbc.fetchone()
else:
    musicdata=None

misc.writebin('Status: 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n');
misc.include(misc.privfile('htmlhead.html'))
if musicdata:
    misc.writebin('''<script language="javascript" type="text/javascript">
midname=getshebang() || %s;
</script>
''' % repr(musicdata[4]));
else:
    misc.writebin('''<script language="javascript" type="text/javascript">
midname=getshebang() || "demo";
</script>
''');
misc.include(misc.privfile('banner.html'))
misc.include(misc.privfile('play.html'))
misc.include(misc.privfile('htmlfoot.html'))
