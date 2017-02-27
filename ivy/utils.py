# --------------------------------------------------------------------------
# Utility functions.
# --------------------------------------------------------------------------

import os
import shutil
import unicodedata
import re

from . import hooks


# Clear the contents of a directory.
def cleardir(dirpath):
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
def copydir(srcdir, dstdir, noclobber=False):

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
def copyfile(src, dst, noclobber=False):
    if os.path.isfile(dst):
        if noclobber:
            return
        if os.path.getmtime(src) == os.path.getmtime(dst):
            if os.path.getsize(src) == os.path.getsize(dst):
                return
    shutil.copy2(src, dst)


# Write a string to a file. Creates parent directories if required.
def writefile(path, content):
    path = os.path.abspath(path)

    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)


# Default slug-preparation function; returns a slugified version of the
# supplied string. This function is used to sanitize url components, etc.
def slugify(arg):
    out = unicodedata.normalize('NFKD', arg)
    out = out.encode('ascii', 'ignore').decode('ascii')
    out = out.lower()
    out = out.replace("'", '')
    out = re.sub(r'[^a-z0-9-]+', '-', out)
    out = re.sub(r'--+', '-', out)
    out = out.strip('-')
    return hooks.filter('slugify', out, arg)
