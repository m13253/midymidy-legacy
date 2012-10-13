#!/usr/bin/env python3

import os
import sys
import config

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

