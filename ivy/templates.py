# --------------------------------------------------------------------------
# This module handles template-engine callbacks.
# --------------------------------------------------------------------------

import sys
import pathlib

from . import site
from . import utils


# Stores registered template-engine callbacks indexed by file extension.
callbacks = {}


# Caches a list of the theme's template files.
cache = None


# Decorator function for registering template-engine callbacks. A template-
# engine callback should accept a Page instance and a template filename and
# return a string of html.
#
# Callbacks are registered per file extension, e.g.
#
#   @ivy.templates.register('ibis')
#   def callback(page, filename):
#       ...
#       return html
#
def register(ext):

    def register_callback(callback):
        callbacks[ext] = callback
        return callback

    return register_callback


# Render a Page instance into html.
def render(page):

    # Cache a list of the theme's template files for future calls.
    global cache
    if cache is None:
        root = site.theme('templates')
        cache = [p for p in pathlib.Path(root).iterdir() if p.is_file()]

    # Find the first template file matching the page's template list.
    for name in page['templates']:
        for path in cache:
            if name == path.stem:
                if path.suffix.strip('.') in callbacks:
                    return callbacks[path.suffix.strip('.')](page, path.name)
                else:
                    msg = "Error: unrecognised template extension '%s'."
                    sys.exit(msg % path.suffix)

    # Missing template file. Print an error message and exit.
    msg = "Error: missing template file for page: '%s'."
    sys.exit(msg % page['filepath'])
