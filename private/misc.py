#!/usr/bin/env python3

import sys

def printfile(ifilename, ostream=sys.stdout):
    with open(ifilename, "r") as istream:
        ostream.write(istream.read(4096))

