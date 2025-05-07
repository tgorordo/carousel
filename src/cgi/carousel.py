#!/usr/bin/env -S uv run python

import os
from dotenv import load_dotenv

load_dotenv()
logdir = os.getenv("CAROUSEL_LOGDIR")

import cgi, cgitb

cgitb.enable(display=0, logdir=logdir)

form = cgi.FieldStorage()

from ..carousel import *

print("Content-Type: text/html")
print()

print("<title>Carousel Matches!</title>")
print("<h1>Carousel Stable Matches Found:</h1>")

print("TODO - INPUTH ECHO NOT IMPLEMENTED")
print("TODO - OUTPUT NOT IMPLEMENTED")
