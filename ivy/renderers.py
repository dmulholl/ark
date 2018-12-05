# ------------------------------------------------------------------------------
# This module handles rendering-engine callbacks. Rendering engines like
# Markdown are responsible for converting raw text input into html.
# ------------------------------------------------------------------------------

import sys
from typing import Dict, Callable


# This dictionary maps text formats to registered rendering-engine callbacks.
# We include a default set of null renderers for various common file
# extensions. (These can be overridden by plugins if desired.) A null renderer
# will simply pass the text straight through without making any changes.
_callbacks: Dict[str, Callable] = {
    'css': lambda s: s,
    'html': lambda s: s,
    'js': lambda s: s,
    'meta': lambda s: s,
    'txt': lambda s: s,
    '': lambda s: s,
}


# Decorator function for registering rendering-engine callbacks. A rendering-
# engine callback should accept an input string containing the text to be
# rendered and return an output string containing the rendered html.
#
# Callbacks are registered per file extension. More than one file extension can
# be specified, e.g.
#
#   @ivy.renderers.register('md', 'mdk')
#   def callback(text):
#       ...
#       return rendered
#
def register(*extensions: str) -> Callable:

    def register_callback(func: Callable) -> Callable:
        for extension in extensions:
            _callbacks[extension] = func
        return func

    return register_callback


# Render a string and return the result.
def render(text: str, ext: str) -> str:
    if ext in _callbacks:
        return _callbacks[ext](text)
    else:
        sys.exit(f"Error: no registered renderer for '.{ext}'.")


# Return true if a rendering-engine callback has been registered for the
# specified file extension.
def is_registered_ext(ext: str) -> bool:
    return ext in _callbacks
