#!/usr/bin/env python3

import cgi
import os
import sqlite3
import json
import time

import config
from misc import *

def main():
    req=cgi.FieldStorage()
    if 'id' in req:
        db=sqlite3.connect(datafile('midymidy.db'))
        dbc=db.cursor()
        dbc.execute('SELECT id, title, desc, filename, time, uploader FROM music WHERE id=?;', (req['id'].value,))
        musicdata=dbc.fetchone()
        if musicdata:
            musicdata=dict(zip(('id', 'title', 'desc', 'filename', 'time', 'uploader'), musicdata))
    else:
        musicdata=None

    if not musicdata:
        prbin('Status: 404 Not Found\r\n\r\n')
        exit()

    prbin('Status: 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n');
    prfile(privfile('htmlhead.html'))
    prbin('''<title>'''+escape_for_html(musicdata['title'])+''' - MidyMidy</title>
<meta name="title" content="'''+escape_for_prop(musicdata['title'])+'''" />
<meta name="description" content="'''+escape_for_prop(musicdata['desc'])+'''" />
''')
    prfile(privfile('banner.html'))
    prbin(
    '''<section itemscope itemtype="http://schema.org/MusicRecording">
<div style="width: 100%; font-size: 32pt; font-weight: bold"><span itemprop="name">'''+escape_for_html(musicdata['title'])+'''</span></div>
<div style="width: 100%; text-align: right">发布时间：<span><meta itemprop="datePublished" content="'''+
    escape_for_html(time.strftime("Y-%m-%dT%H:%M:%S%z", time.gmtime(musicdata['time'])))+
    '''" />'''+
    escape_for_html(time.strftime("%c", time.localtime(musicdata['time'])))+
    '''</span>，发布者&nbsp;ID：<span itemprop="author">'''+escape_for_html(musicdata['uploader'])
    +'''</span></div>
<hr />
<audio itemprop="audio" controls="controls" style="width: 1024px" id="audio" preload="preload" ontimeupdate="score=document.getElementById('score').contentWindow; score.scrollTo(0, (this.currentTime+score.mintime)*32);">
<source src="midi/'''+escape_for_prop(musicdata['filename'])+'''.ogg" type="audio/ogg; codec=vorbis" />
<div style="font-size: 32px; color: red">Error: Your browser does not support HTML5 audio replay.</div>
</audio>
<iframe width="1024" height="640" seamless="seamless" scrolling="no" frameborder="0" style="border: none; overflow: hidden" src="about:blank" id="score"></iframe>
<script language="javascript" type="text/javascript">
document.getElementById("score").src="preview.html#!midi/'''+escape_for_js(musicdata['filename'])+'''.mid";
var audio=document.getElementById("audio");
audio.addEventListener("error", function() {
    console.log("File type not supported.");
    throw "File type not supported.";
}, true);
</script>
<hr />
<div style="font-weight: bold">简介：</div>
<blockquote><span itemprop="description">'''+escape_for_html(musicdata['desc'])+'''</span></blockquote>
</section>
''');
    prfile(privfile('htmlfoot.html'))

if __name__=='__main__':
    runmain(main)

