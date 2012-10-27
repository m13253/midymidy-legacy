#!/usr/bin/env python3

import cgi
import json
import os
import sys
import traceback

import config

def runmain(func):
    try:
        return func()
    except SystemExit:
        raise
    except Exception:
        if config.print_debug_on_error:
            e=sys.exc_info()
            try:
                prbin('<big><pre>\n'+cgi.escape(''.join(traceback.format_exception(e[0], e[1], e[2])))+'\n</pre></big>')
            except:
                pass
        else:
            try:
                prbin('<h1>\nAn error occured during handling of your request. We apologize for the inconvenience.\n</h1>')
            except:
                pass

def prfile(ifilename, ostream=sys.stdout):
    with open(ifilename, 'rb') as istream:
        while True:
            buf=istream.read(4096)
            if buf:
                prbin(buf, ostream)
            else:
                break

def prbin(istr, ostream=sys.stdout):
    if isinstance(istr, bytes):
        return ostream.buffer.write(istr)
    else:
        return ostream.buffer.write(istr.encode('utf-8', 'replace'))

def privfile(filename=None):
    if filename==None:
        return config.private_dir
    else:
        return os.path.join(config.private_dir, filename);

def datafile(filename=None):
    if filename==None:
        return config.private_dir
    else:
        return os.path.join(config.database_dir, filename);

def escape_for_js(s):
    return json.dumps(str(s))[1:-1]

def escape_for_html(s):
    return cgi.escape(str(s))

def escape_for_prop(s):
    return escape_for_html(s).replace('"', '&quot;').replace("'", '&apos;')

def error_page(status, msg):
    if status!=None:
        prbin('Status: %s\r\nContent-Type: text/html; charset=utf-8\r\n\r\n')
    if msg!=None:
        prfile(privfile('htmlhead.html'))
        prbin('''<title>Error - MidyMidy</title>''')
        prfile(privfile('banner.html'))
        prbin('''<h2>%s</h2>''' % msg)
        prfile(privfile('htmlfoot.html'))

