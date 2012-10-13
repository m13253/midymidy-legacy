#!/usr/bin/env python3

import config
import misc

misc.writebin("Status: 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n");
misc.include("play.html")
