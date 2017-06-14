#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# ExifMoveAndSort by Nicolas Meier
# Move and sort pictures by using Exiftool and Hazel
# https://github.com/nicolasm/ExifMoveAndSort
# Last revsion: May 28, 2017
# Pictures are moved to the Photos repository and sorted by Exif original date
# ExifTool (http://www.sno.phy.queensu.ca/~phil/exiftool/)

import re
import subprocess
import sys
import os
import locale

def is_running(process):
    s = subprocess.Popen(["ps", "axw"],stdout=subprocess.PIPE)
    for x in s.stdout:
        if re.search(process, x):
            return True

    return False

file = sys.argv[1]
if os.path.isdir(file):
    path = file
else:
    path = os.path.dirname(os.path.abspath(file))

target = ""
# Set the final directory according to the source
if os.path.samefile(path, "/home/nicolas/Pictures/Approved"):
     target = ""
elif os.path.samefile(path, "/home/nicolas/Pictures/Phone"):
     target = "Phone"

# Force the locale to fr_FR.UTF-8
env = os.environ.copy()
env['LANG'] = 'fr_FR.UTF-8'

# Ensure PhotoReviewer, Phoenix Slides and PhotoSync are not running
if not (is_running(b"PhotoReviewer\.app") or is_running(b"Phoenix Slides\.app") or is_running(b"PhotoSync\.app")):
    s = subprocess.Popen(["exiftool", "-Directory<DateTimeOriginal", "-d", "/home/nicolas/Pictures/Photos/%Y/%m - %B/" + target, path], stdout=subprocess.PIPE, env = env)
    message = ""
    for x in s.stdout:
        message = message + x.decode("utf-8")

print(message)
