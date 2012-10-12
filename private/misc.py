#!/usr/bin/env python3

import sys

def include(ifilename, ostream=sys.stdout):
    with open(ifilename, "rb") as istream:
        while True:
            buf=istream.read(4096)
            if buf:
                ostream.buffer.write(buf)
            else:
                break

