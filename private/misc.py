#!/usr/bin/env python3

import sys

def printfile(ifilename, ostream=sys.stdout):
    with open(ifilename, "r") as istream:
        while True:
            buf=istream.read(4096)
            if buf:
                ostream.write(buf)
            else:
                break

