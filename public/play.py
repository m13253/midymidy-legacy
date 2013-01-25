#!/usr/bin/env python3

import cgi
import sqlite3
import time

import config
from misc import *
import dbman

def main():
    if detect_ie():
        exit()

    req=cgi.FieldStorage()
    if 'id' in req:
        try:
            musicdata=dbman.getmusicdata(req['id'].value, ('title', 'desc', 'ctime', 'uploader', 'filename'))
        except ValueError:
            musicdata=None
        if not musicdata:
            prbin('Status: 404 Not Found\r\n\r\n')
            exit()
    else:
        prbin('Status: 301 Moved Permanently\r\nLocation: ?id=md2\r\n\r\n')
        exit()

    prbin('Status: 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n');

    prfile(privfile('htmlhead.html'))

    prbin(
'''<title>'''+escape_for_html(musicdata['title'])+''' - MidyMidy</title>
<meta name="title" content="'''+escape_for_prop(musicdata['title'])+'''" />
<meta name="description" content="'''+escape_for_prop(musicdata['desc'])+'''" />
''')

    prfile(privfile('banner.html'))

    prbin(
'''<section itemscope itemtype="http://schema.org/MusicRecording">
<h1><span itemprop="name">'''+escape_for_html(musicdata['title'])+'''</span></h1>
<div style="width: 100%; text-align: right">发布时间：<span><meta itemprop="datePublished" content="'''+escape_for_html(time.strftime("%Y-%m-%dT%H:%M:%S%z", time.gmtime(musicdata['ctime'])))+'''" />'''+escape_for_html(time.strftime("%c", time.localtime(musicdata['ctime'])))+'''</span>，发布者&nbsp;ID：<span itemprop="author">'''+escape_for_html(musicdata['uploader'])+'''</span></div>
<hr />
<audio itemprop="audio" controls="controls" style="width: 100%" id="audio">
<source src="midi/'''+escape_for_prop(musicdata['filename'])+'''.ogg" type="audio/ogg; codec=vorbis" />
<div style="font-size: 32px; color: red">错误：您的浏览器不支持&nbsp;HTML5&nbsp;音频回放。</div>
</audio>
<div id="preview" style="width: 100%; background-color: lightgray; color: red; text-align: center; font-size: 16pt"><noscript>错误：您需要&nbsp;Javascript&nbsp;来启用实时预览。</noscript></div>
<script language="javascript" type="text/javascript">
previewdiv=document.getElementById("preview");
previewdiv.innerHTML="<img src=\\"loading.gif\\" valign=\\"middle\\" />正在加载实时预览……"
previewdiv.style.backgroundColor="";
previewdiv.style.color="";
audio=document.getElementById("audio");
audio.addEventListener("error", function() {
    previewdiv.innerHTML="错误：无法启动音频回放。"
    previewdiv.style.backgroundColor="lightgray";
    previewdiv.style.color="red";
}, true);
score=null;
audio.addEventListener("canplay", function() {
    previewdiv.style.backgroundColor="";
    previewdiv.style.color="";
    previewdiv.innerHTML="<iframe width=\\"1024\\" height=\\"640\\" seamless=\\"seamless\\" scrolling=\\"no\\" frameborder=\\"0\\" style=\\"border: none; overflow: hidden\\" src=\\"preview.html#!midi/'''+escape_for_js(musicdata['filename'])+'''.mid\\" id=\\"score\\"></iframe>"
    score=document.getElementById("score").contentWindow;
}, true);
audio.addEventListener("timeupdate", function() {
    if(score)
        score.scrollTo(0, audio.currentTime*32);
}, true);
audio.load();
</script>
<hr />
<div style="font-weight: bold">简介：</div>
<blockquote><span itemprop="description">'''+escape_for_html(musicdata['desc'])+'''</span></blockquote>
</section>
''');

    prfile(privfile('htmlfoot.html'))

if __name__=='__main__':
    runmain(main)

