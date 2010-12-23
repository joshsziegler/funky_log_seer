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
