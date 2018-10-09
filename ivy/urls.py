# ------------------------------------------------------------------------------
# This module handles @root/ url rewriting.
# ------------------------------------------------------------------------------

import re
import os

from . import site


# Regex for locating @root/ urls for rewriting. We only rewrite urls inside
# quotes (which are preserved) or angle brackets (which evaporate).
re_url = re.compile(r'''(["'<])@root/(.*?)(#.*?)?(\1|>)''')


# Rewrite all @root/ urls to their final form.
def rewrite(html: str, filepath: str):
    relpath = os.path.relpath(filepath, site.out())
    depth = len(relpath.replace('\\', '/').split('/'))
    prefix = site.config.get('root') or '../' * (depth - 1)
    suffix = site.config.get('extension')

    # Each matched url is replaced with the output of this callback.
    def callback(match):
        quote = match.group(1) if match.group(1) in ('"', "'") else ''
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

        return '%s%s%s%s' % (quote, url, fragment, quote)

    # Replace each match with the return value of the callback.
    return re_url.sub(callback, html)
