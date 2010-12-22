#!/usr/bin/python26

import cgi
import sys

sys.path.append('/usr/lib/python2.4/site-packages/')
sys.path.append('/usr/lib64/python2.4/site-packages/')
from mako.lookup import TemplateLookup
from mako.template import Template
from mako.runtime import Context
from StringIO import StringIO
from mako import exceptions

LOG_DIR = "/var/log/remotesystems/"

def reversed_lines(file):
    """Generate the lines of file in reverse order.
        
       http://stackoverflow.com/questions/260273/most-efficient-way-to-search-the-last-x-lines-of-a-file-in-python/260433#260433
    """
    tail = []           # Tail of the line whose head is not yet read.
    for block in reversed_blocks(file):
        # A line is a list of strings to avoid quadratic concatenation.
        # (And trying to avoid 1-element lists would complicate the code.)
        linelists = [[line] for line in block.splitlines()]
        linelists[-1].extend(tail)
        for linelist in reversed(linelists[1:]):
            yield ''.join(linelist)
        tail = linelists[0]
    if tail: yield ''.join(tail)

def reversed_blocks(file, blocksize=4096):
    "Generate blocks of file's contents in reverse order."
    import os

    file.seek(0, os.SEEK_END)
    here = file.tell()
    while 0 < here:
        delta = min(blocksize, here)
        file.seek(here - delta, os.SEEK_SET)
        yield file.read(delta)
        here -= delta

def get_log_files():
    """Returns array of tuples with the log's name and path.
    """
    import os
    results = {} 
    for root, dirs, files in os.walk(LOG_DIR):
        for log in files:
            log_name = log.replace(".log", "")
            results[log_name] =  os.path.join(root, log)
    return results 

def grep(pattern, file_obj, top_to_bottom=False, include_line_nums=False):
    # TODO: Add option to flip these results around
    import re
    if not top_to_bottom:
        file_obj = reversed_lines(file_obj)

    try:
        grepper = re.compile(pattern)
        for line_num, line in enumerate(file_obj):
            line =  line.replace("\n", "")
            if grepper.search(line):
                if include_line_nums:
                    yield (line_num, line)
                else:
                    yield line
    except Exception, e:
         print "<p>Error in regex!</p>" 
         print e

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def show_headers():
    print "Content-type: text/html" 
    print ""

def main():
    show_headers()

    form = cgi.FieldStorage()
    buf = StringIO()

    log_files = get_log_files()

    limit = 25
    top_to_bottom = False
    regex = "."

    if form.has_key("limit"):
        limit = int(form.getvalue("limit"))
        if not is_number(limit) or limit < 0 or limit > 501:
            limit = 25

    if form.has_key("toptobottom") and form.getvalue("toptobottom") == "true":
        top_to_bottom = True 
            
    if form.has_key("regex") and form.getvalue("regex") != "":
        regex = form.getvalue("regex")

    if form.has_key("file") and form.getvalue("file") != "":
        file_name = form.getvalue("file")
        file_path = log_files[file_name]
        srch_rslt = []
        for count, res in  enumerate(grep(regex, file(file_path, 'r'), top_to_bottom)):
            if count < limit:
                res = res.split(file_name, 1)
                #res = [res[0]].extend(res[1].split(":", 1))
                srch_rslt.append((res[0], file_name, res[1]))
            else:
                break
        ctx = Context(buf, page_title="FLS",app_name="Funky Log Seer", search_page="index.py", log_results=srch_rslt, file_options=log_files)
    else: # TODO: Make this the same as above, using the list files_to_search
        files_to_search = log_files.keys()
        srch_rslt = []
        count = 0
        for file_name in files_to_search:
            if count < limit:
                file_path = log_files[file_name]
                for res in grep(regex, file(file_path,'r'), top_to_bottom):
                    if count < limit:
                        res = res.split(file_name, 1)
                        #res = [res[0]].extend(res[1].split(":", 1))
                        srch_rslt.append((res[0], file_name, res[1]))
                        count += 1
                    else:
                        break
            else:
                break
            
        ctx = Context(buf, page_title="FLS",app_name="Funky Log Seer", search_page="index.py", log_results=srch_rslt, file_options=log_files)

    try:
        mylkup = TemplateLookup(directories=['templates/'])
        mytemp = Template(filename='templates/index.mako', lookup=mylkup)
        mytemp.render_context(ctx)
    except:
        print exceptions.text_error_template().render()

    print buf.getvalue()

if __name__ == '__main__':
     main()

