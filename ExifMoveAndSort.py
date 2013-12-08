#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# ExifMoveAndSort by Nicolas Meier
# Move and sort pictures by using Exiftool and Hazel
# https://github.com/nicolasm/ExifMoveAndSort
# Last revsion: Oct 6, 2013
# Pictures are moved to the Photos repository and sorted by Exif original date
# ExifTool (http://www.sno.phy.queensu.ca/~phil/exiftool/)

import re
import subprocess
import gntp.notifier
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
if os.path.samefile(path, "/Users/YourUser/path/to/Camera Roll"):
    target = "iPhone"
elif os.path.samefile(path, "/Users/YourUser/path/to/incoming"):
     target = ""

# Force the locale to fr_FR.UTF-8 because Hazel use the wrong locale
env = os.environ.copy()
env['LANG'] = 'fr_FR.UTF-8'

# Ensure PhotoReviewer, Phoenix Slides and PhotoSync are not running
if not (is_running("PhotoReviewer\.app") or is_running("Phoenix Slides\.app") or is_running("PhotoSync\.app")):
    s = subprocess.Popen(["exiftool", "-Directory<DateTimeOriginal", "-d", "/path/to/target/%Y/%m - %B/" + target, path], stdout=subprocess.PIPE, env = env)
    message = ""
    for x in s.stdout:
        message = message + x

    gntp.notifier.mini(message)