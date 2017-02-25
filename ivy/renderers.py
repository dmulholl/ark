# --------------------------------------------------------------------------
# This module handles text-to-html rendering-engine callbacks.
# --------------------------------------------------------------------------

import sys


# This dictionary maps text formats to registered rendering-engine
# callbacks. We include a default set of null renderers for various common
# file extensions. (These can be overridden by plugins if desired.) A null
# renderer will simply pass the text straight through without making any
# changes.
callbacks = {
    'css': lambda s: s,
    'html': lambda s: s,
    'js': lambda s: s,
    'meta': lambda s: s,
    'txt': lambda s: s,
    '': lambda s: s,
}


# Decorator function for registering rendering-engine callbacks. A rendering-
# engine callback should accept an input string and return a string containing
# the rendered html.
#
# Callbacks are registered per file extension, e.g.
#
#   @ivy.renderers.register('md')
#   def callback(text):
#       ...
#       return rendered
#
def register(ext):

    def register_callback(callback):
        callbacks[ext] = callback
        return callback

    return register_callback


# Render a string and return the result.
def render(text, ext):
    if ext in callbacks:
        return callbacks[ext](text)
    else:
        sys.exit("Error: no registered renderer for '.%s'." % ext)
