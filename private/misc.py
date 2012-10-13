#!/usr/bin/env python3

import sys

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

