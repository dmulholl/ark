# ------------------------------------------------------------------------------
# This module contains utility functions used throughout the application.
# ------------------------------------------------------------------------------

import os
import shutil
import re
import sys
import unicodedata

from . import filters
from . import site


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
# input string. This function is used to sanitize url components, etc.
def slugify(input_string: str) -> str:
    if custom_slug := filters.apply('slugify', None, input_string):
        return custom_slug
    output = unicodedata.normalize('NFKD', input_string)
    output = output.encode('ascii', errors='ignore').decode('ascii')
    output = output.lower()
    output = output.replace("'", '')
    output = re.sub(r'[^a-z0-9-]+', '-', output)
    output = re.sub(r'--+', '-', output)
    return output.strip('-')


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


# Print a grey line across the width of the terminal.
def termline():
    cols, _ = shutil.get_terminal_size()
    line = '\u001B[90m' + '─' * cols + '\u001B[0m'
    safeprint(line)


# Regex for locating @root/ urls enclosed in quotes.
regex_url = re.compile(r"""
    (["'])@root/(.*?)([#].*?)?\1
""", re.VERBOSE)


# Rewrite all @root/ urls in the HTML document to their final form.
def rewrite_urls(html: str, filepath: str):
    relpath = os.path.relpath(filepath, site.out())
    depth = len(relpath.replace('\\', '/').split('/'))
    prefix = site.config.get('root') or '../' * (depth - 1)
    suffix = site.config.get('extension')

    # Each matched url is replaced with the output of this callback.
    def callback(match):
        quote = match.group(1)
        url = match.group(2).lstrip('/') if match.group(2) else ''
        fragment = match.group(3) or ''

        # 1. We have a link to the homepage.
        if url == '':
            if suffix == '/':
                if depth == 1:
                    url = '' if fragment else '#'
                else:
                    url = prefix
            else:
                url = prefix + 'index' + suffix

        # 2. We have a link to a generated node page.
        elif url.endswith('//'):
            if suffix == '/':
                url = prefix + url.rstrip('/') + '/'
            else:
                url = prefix + url.rstrip('/') + suffix

        # 3. We have a link to a static asset or directory.
        else:
            url = prefix + url

        return f"{quote}{url}{fragment}{quote}"

    # Replace each match with the return value of the callback.
    return regex_url.sub(callback, html)


# Load a source file. The `path` parameter can be either a string or a
# pathlib.Path instance. File metadata (e.g. yaml headers) can be extracted by
# preprocessor callbacks registered on the 'file_text' filter hook.
def loadfile(path):
    try:
        with open(str(path), encoding='utf-8') as file:
            text, meta = file.read(), {}
        text = filters.apply('file_text', text, meta)
        for key, value in list(meta.items()):
            normalized_key = key.lower().replace(' ', '_').replace('-', '_')
            if normalized_key != key:
                del meta[key]
                meta[normalized_key] = value
        return text, meta
    except Exception as err:
        msg = f"Error loading file: {path}\n"
        msg += f">> {err.__class__.__name__}: {err}"
        if (cause := err.__cause__):
            msg += f"\n>> Cause: {cause.__class__.__name__}: {cause}"
        elif (context := err.__context__):
            msg += f"\n>> Context: {context.__class__.__name__}: {context}"
        sys.exit(msg)
