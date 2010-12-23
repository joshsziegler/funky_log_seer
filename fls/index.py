#!/usr/bin/python

import cgi
import sys

from mako.lookup import TemplateLookup
from mako.template import Template
from mako.runtime import Context
from StringIO import StringIO
from mako import exceptions

from shared import utils   

LOG_DIR = "/var/log/"

def show_headers():
    print "Content-type: text/html" 
    print ""

def get_user_args(form, log_files):
    # Setup defaults for user inputs
    limit = 25
    top_to_bottom = False
    regex = "."
    files_to_search = []

    # Check input for size, type and valid values
    if form.has_key("limit"):
        limit = int(form.getvalue("limit"))
        if not utils.is_number(limit) or limit < 0 or limit > 10001:
            limit = 25

    if form.has_key("toptobottom") and form.getvalue("toptobottom") == "true":
        top_to_bottom = True 
            
    regex = form.getvalue("regex")
    if form.has_key("regex") and regex != "" and len(regex) < 50:
        regex = form.getvalue("regex")
    else:
        regex = "."

    if form.has_key("file") and form.getvalue("file") != "":
        files_to_search = [form.getvalue("file")]
    else:
        files_to_search = log_files.keys()

    return limit, top_to_bottom, regex, files_to_search

def main():
    show_headers()

    form = cgi.FieldStorage()
    html_output = StringIO() 
    log_files = utils.get_log_files(LOG_DIR)
    limit, top_to_bottom, regex, files_to_search = get_user_args(form, log_files)

    srch_rslt = []
    result_count = 0
    for file_name in files_to_search:
        if result_count < limit:
            # Note we only allow files to be searched if they exist in this dict
            # Otherwise a user could traverse the filesystem and read in /etc/passwd!
            file_path = log_files[file_name]
            for result in utils.grep(regex, file(file_path,'r'), top_to_bottom):
                if result_count < limit:
                    # This assumes a syslog format (Date hostname program : content)
                    res_split = result.split(file_name, 1)
                    #res = [res[0]].extend(res[1].split(":", 1))
                    try:
                        srch_rslt.append((res_split[0], file_name, res_split[1]))
                    except:
                        srch_rslt.append((file_name, result))
                    result_count += 1
                else:
                    break
        else:
            break
        
    ctx = Context(html_output, page_title="FLS",app_name="Funky Log Seer", search_page="index.py", log_results=srch_rslt, file_options=log_files)
    # Try to lookup the template and to render it using our context
    try:
        mylkup = TemplateLookup(directories=['templates/'])
        mytemp = Template(filename='templates/index.mako', lookup=mylkup)
        mytemp.render_context(ctx)
    except:
        print exceptions.text_error_template().render()

    # Print the resulting HTML 
    print html_output.getvalue()

if __name__ == '__main__':
     main()

