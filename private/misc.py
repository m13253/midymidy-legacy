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
                writebin('<big><pre>'+cgi.escape(''.join(traceback.format_exception(e[0], e[1], e[2])))+'</pre></big>')
            except:
                pass
        else:
            try:
                writebin('<h1>An error occured during handling of your request. We are sorry for the inconvenience.</h1>')
            except:
                pass

def include(ifilename, ostream=sys.stdout):
    with open(ifilename, 'rb') as istream:
        while True:
            buf=istream.read(4096)
            if buf:
                writebin(buf, ostream)
            else:
                break

def writebin(istr, ostream=sys.stdout):
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
    return json.dumps(s)[1:-1]

escape_for_html=cgi.escape

def escape_for_prop(s):
    return escape_for_html(s).replace('"', '&quot;').replace("'", '&apos;')

