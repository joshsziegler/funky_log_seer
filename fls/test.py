#!/usr/bin/python

import cgi
import sys
from mako.lookup import TemplateLookup
from mako.template import Template
from mako.runtime import Context
from StringIO import StringIO
from mako import exceptions

LOG_DIR = "/var/log/remotesystems/"

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

def grep(pattern, file_obj, include_line_nums=False):
    # TODO: Add option to flip these results around
    import re
    grepper = re.compile(pattern)
    for line_num, line in enumerate(file_obj):
        line =  line.replace("\n", "")
        if grepper.search(line):
            if include_line_nums:
                yield (line_num, line)
            else:
                yield line

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

    if form.has_key("limit"):
        limit = form.getvalue("limit")
        if not is_number(limit) or limit < 0 or limit > 501:
            limit = 25

    if form.has_key("regex") and form.getvalue("regex") != "":
        regex = form.getvalue("regex")
        if form.has_key("file") and form.getvalue("file") != "":
            file_name = form.getvalue("file")
            file_path = log_files[file_name]
            srch_rslt = []
            for count, res in  enumerate(grep(regex, file(file_path, 'r'))):
                if count < limit:
                    srch_rslt.append((file_name, res))
                else:
                    break
            ctx = Context(buf, page_title="FLS",app_name="Funky Log Seer", search_page="test.py", log_results=srch_rslt, file_options=log_files)
        else: # TODO: Make this the same as above, using the list files_to_search
            files_to_search = log_files.keys()
            srch_rslt = []
            count = 0
            for file_name in files_to_search:
                if count < limit:
                    file_path = log_files[file_name]
                    for res in grep(regex, file(file_path,'r')):
                        if count < limit:
                            srch_rslt.append((file_name, res))
                            count += 1
                        else:
                            break
                else:
                    break
            
            ctx = Context(buf, page_title="FLS",app_name="Funky Log Seer", search_page="test.py", log_results=srch_rslt, file_options=log_files)
    else:
        ctx = Context(buf, page_title="FLS",app_name="Funky Log Seer", search_page="test.py", log_results=[], file_options=log_files)

    try:
        mylkup = TemplateLookup(directories=['templates/'])
        mytemp = Template(filename='templates/index.mako', lookup=mylkup)
        mytemp.render_context(ctx)
    except:
        print exceptions.text_error_template().render()

    print buf.getvalue()

if __name__ == '__main__':
     main()

