# ------------------------------------------------------------------------------
# This module contains utility functions used throughout the application.
# ------------------------------------------------------------------------------

import os
import shutil
import unicodedata
import re
import sys

from . import hooks


# Clear the contents of a directory.
def cleardir(dirpath: str):
    if os.path.isdir(dirpath):
        for name in os.listdir(dirpath):
            path = os.path.join(dirpath, name)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)


# Copy the contents of 'srcdir' to 'dstdir'. The destination directory will be
# created if it does not already exist. If 'noclobber' is true, existing files
# will not be overwritten.
def copydir(srcdir: str, dstdir: str, noclobber: bool = False):

    if not os.path.exists(srcdir):
        return

    if not os.path.exists(dstdir):
        os.makedirs(dstdir)

    for name in os.listdir(srcdir):
        src = os.path.join(srcdir, name)
        dst = os.path.join(dstdir, name)

        if name in ('__pycache__', '.DS_Store'):
            continue

        if os.path.isfile(src):
            copyfile(src, dst, noclobber)
        elif os.path.isdir(src):
            copydir(src, dst, noclobber)


# Copy the file 'src' as 'dst'. If 'noclobber' is true, an existing 'dst' file
# will not be overwritten. This function attempts to avoid unnecessarily
# overwriting existing files with identical copies. If 'dst' exists and has
# the same size and mtime as 'src', the copy will be aborted.
def copyfile(src: str, dst: str, noclobber: bool = False):
    if os.path.isfile(dst):
        if noclobber:
            return
        if os.path.getmtime(src) == os.path.getmtime(dst):
            if os.path.getsize(src) == os.path.getsize(dst):
                return
    shutil.copy2(src, dst)


# Write a string to a file. Creates parent directories if required.
def writefile(path: str, content: str):
    path = os.path.abspath(path)

    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)


# Default slug-preparation function; returns a slugified version of the
# supplied string. This function is used to sanitize url components, etc.
def slugify(string: str) -> str:
    out = unicodedata.normalize('NFKD', string)
    out = out.encode('ascii', errors='ignore').decode('ascii')
    out = out.lower()
    out = out.replace("'", '')
    out = re.sub(r'[^a-z0-9-]+', '-', out)
    out = re.sub(r'--+', '-', out)
    out = out.strip('-')
    return hooks.filter('slugify', out, string)


# A drop-in replacement for the print function that won't choke when
# attempting to print unicode characters to a non-unicode terminal. Known
# problem characters are replaced with ascii alternatives; any other
# unprintable characters are replaced with a '?'.
def safeprint(*objects, sep=' ', end='\n', file=sys.stdout):
    if file.encoding.lower() == 'utf-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        strings, enc = [], file.encoding
        for obj in objects:
            string = str(obj).replace('─', '-').replace('·', '|')
            string = string.encode(enc, errors='replace').decode(enc)
            strings.append(string)
        print(*strings, sep=sep, end=end, file=file)
