#!/usr/bin/env python3

import config
import misc
import os

misc.writebin("Status: 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n");
misc.include(misc.privfile("htmlhead.html"))
misc.include(misc.privfile("banner.html"))
misc.include(misc.privfile("play.html"))
misc.include(misc.privfile("htmlfoot.html"))
