#!/usr/bin/python

# Copyright 2010 Josh Ziegler
#
# This file is part of Funky Log Seer (FLS) 
#
# Funky Log Seer (FLS) is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Funky Log Seer (FLS) is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Funky Log Seer (FLS). If not, see <http://www.gnu.org/licenses/>.

import fnmatch
import os

DEFAULT_LOG_DIR = "/var/log"

matches = []
for root, dirnames, filenames in os.walk('/'):
  for filename in fnmatch.filter(filenames, '*.log'):
        matches.append(os.path.join(root, filename))

f = open('logfiles', 'w')
for log in matches:
    f.write("#" + log + "\n")

# Add everything in the log directory
for root, dirs, files in os.walk(DEFAULT_LOG_DIR):
    for log in files:
        f.write("#" + os.path.join(root, log) + "\n")

f.close()