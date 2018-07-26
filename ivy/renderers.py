# ------------------------------------------------------------------------------
# This module handles rendering-engine callbacks. Rendering engines like
# Markdown are responsible for converting raw text input into html.
# ------------------------------------------------------------------------------

import sys
from typing import Dict, Callable


# This dictionary maps text formats to registered rendering-engine
# callbacks. We include a default set of null renderers for various common
# file extensions. (These can be overridden by plugins if desired.) A null
# renderer will simply pass the text straight through without making any
# changes.
callbacks: Dict[str, Callable[[str], str]] = {
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
def register(ext: str) -> Callable:

    def register_callback(callback: Callable[[str], str]):
        callbacks[ext] = callback
        return callback

    return register_callback


# Render a string and return the result.
def render(text: str, ext: str) -> str:
    if ext in callbacks:
        return callbacks[ext](text)
    else:
        sys.exit("Error: no registered renderer for '.%s'." % ext)
