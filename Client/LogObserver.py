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

import time
import sys
import os  
import json
import urllib2
import datetime

def get_host_name():
    import platform 
    return platform.node()

SERVERS = ["localhost:5984"]

HOST = get_host_name() 
SERVER = "localhost"
DATABASE_NAME = "logs"
LOG_WATCH_LIST_PATH = "logfiles"


def get_logs_to_watch(log_watch_list_path):
    """return list of logs to watch path
    """
    import re
    log_paths = []

    # Matches lines that start with '#'
    comment = re.compile(r'#.+?') 
    file = open(log_watch_list_path, 'r')

    for line in file:
        if not comment.match(line):
            # If not a comment, add it to the paths to be returned
            log_paths.append(line.rstrip("\n"))
            print "Watching " + line.rstrip("\n")

    return log_paths 

class LogObserver(object):
    """Watches a given log for changes and sends those changes to a central
    CouchDB collection server.
    """
    def __init__(self, host, servers, db_name, log_paths):
        self.host = host
        self.servers = servers
        self.db_name = db_name
        self.log_paths = log_paths

    def start_watch(self):
        """Starts the actual log watch.
        """
        self._setup_and_open_logs()
        self._watch()

    def _setup_and_open_logs(self):
        self.logs = []
        for log_path in self.log_paths:
            log_file = open(log_path,'r')
            # We are only interested in new log entries, so move to the end
            st_results = os.stat(log_path)
            st_size = st_results[6]
            log_file.seek(st_size) # comment this out for simpler debugging (caution: reads all of file)
            self.logs.append(log_file)

    def _watch(self):
        # Continuosly monitor the log files for new lines
        while 1:
            for log in self.logs:
                where = log.tell()
                new_line = log.readline()
                if not new_line:
                    log.seek(where)
                else: # newline found
                    # Send the log entry to the central collection server(s) 
                    for server in self.servers:
                        self._send_line_to_server(server, log.name, new_line)

            time.sleep(5)

    def _send_line_to_server(self, server, log_name, log_line): 
        """Transports the log line to the CouchDB server.
        """
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        # Grab a UUID first
        request = urllib2.Request('http://' + server + '/_uuids')
        try:
            url = opener.open(request)
            response = json.loads(url.read())
            uuid = response['uuids'][0]
        except urllib2.HTTPError, error:
            contents = error.read()

        if uuid:
            # Then create our new document (our log line)
            now = datetime.datetime.now()
            data = json.dumps({"Content": log_line,
                               "Host": self.host,
                               "File": log_name,
                               "Year": now.year,
                               "Month": now.month,
                               "Day": now.day,
                               "Hour": now.hour,
                               #"Tags":["warning", "error" ]
                               })
            request = urllib2.Request('http://'+ server +'/'+ self.db_name +'/'+ uuid, data)
            request.add_header('Content-Type', 'application/json')
            request.get_method = lambda: 'PUT'
            try:
                url = opener.open(request)
                response = json.loads(url.read())
                if response['ok'] != 'True':
                    print "Failed to upload log: " + response
            except urllib2.HTTPError, error:
                contents = error.read()
                print contents

if __name__ == "__main__":
    logs = get_logs_to_watch(LOG_WATCH_LIST_PATH)

    lo = LogObserver(HOST, SERVERS, DATABASE_NAME, logs)
    lo.start_watch()
