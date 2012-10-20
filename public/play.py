#!/usr/bin/env python3

import cgi
import os
import sqlite3
import json

import config
import misc

def main():
    req=cgi.FieldStorage()
    if 'id' in req:
        db=sqlite3.connect(misc.datafile('midymidy.db'))
        dbc=db.cursor()
        dbc.execute('SELECT id, title, desc, filename, time, uploader FROM music WHERE id=?;', (req['id'].value,))
        musicdata=dbc.fetchone()
        if musicdata:
            musicdata=dict(zip(('id', 'title', 'desc', 'filename', 'time', 'uploader'), musicdata))
    else:
        musicdata=None

    if not musicdata:
        misc.writebin('Status: 404 Not Found\r\n\r\n')
        exit()

    misc.writebin('Status: 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n');
    misc.include(misc.privfile('htmlhead.html'))
    misc.writebin('''<title>'''+cgi.escape(musicdata['title'])+''' - MidyMidy</title>
<meta name="title" content="'''+cgi.escape(musicdata['title'])+'''" />
<meta name="description" content="'''+cgi.escape(musicdata['desc'])+'''" />
''')
    misc.include(misc.privfile('banner.html'))
    misc.writebin(
    '''<section itemscope itemtype="http://schema.org/MusicRecording">
<div style="font-size: 32pt; font-weight: bold"><span itemprop="name">'''+cgi.escape(musicdata['title'])+'''</span></div>
<hr />
<audio itemprop="audio" controls="controls" style="width: 1024px" id="audio" preload="preload" ontimeupdate="score=document.getElementById('score').contentWindow; score.scrollTo(0, (this.currentTime+score.mintime)*32);">
<source src="midi/'''+misc.escape(musicdata['filename'])+'''.ogg" type="audio/ogg; codec=vorbis" />
<div style="font-size: 32px; color: red">Error: Your browser does not support HTML5 audio replay.</div>
</audio>
<iframe width="1024" height="640" seamless="seamless" scrolling="no" frameborder="0" style="border: none; overflow: hidden" src="about:blank" id="score"></iframe>
<script language="javascript" type="text/javascript">
document.getElementById("score").src="preview.html#!midi/'''+misc.escape(musicdata['filename'])+'''.mid";
var audio=document.getElementById("audio");
audio.addEventListener("error", function() {
    console.log("File type not supported.");
    throw "File type not supported.";
}, true);
</script>
<hr />
<div style="font-weight: bold">简介：</div>
<blockquote><span itemprop="description">'''+cgi.escape(musicdata['desc'])+'''</span></blockquote>
</section>
''');
    misc.include(misc.privfile('htmlfoot.html'))

if __name__=='__main__':
    misc.runmain(main)

