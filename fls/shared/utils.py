from reversed_lines import reader as rlr

def get_log_files(log_dir):
    """Returns array of tuples with the log's name and path.
    """
    import os
    results = {}
    for root, dirs, files in os.walk(log_dir):
        for log in files:
            log_name = log.replace(".log", "")
            results[log_name] =  os.path.join(root, log)
    return results

def grep(pattern, file_obj, top_to_bottom=False, include_line_nums=False):
    import re
    if not top_to_bottom:
        file_obj = rlr.reversed_lines(file_obj)

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
