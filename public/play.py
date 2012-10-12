#!/usr/bin/env python3

import config
import misc

print("Status: 200 OK")
print("Content-Type: text/html; charset=utf-8");
print()
misc.include("play.html")
