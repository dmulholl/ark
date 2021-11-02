# ------------------------------------------------------------------------------
# This module handles rendering-engine callbacks. Rendering engines like
# Markdown are responsible for converting raw text input into HTML.
# ------------------------------------------------------------------------------

import sys


# This dictionary maps text formats identified by file extension to callback
# functions which render text into html.
_callbacks = {}


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
#       return html
#
def register(*extensions):

    def register_callback(func):
        for extension in extensions:
            _callbacks[extension] = func
        return func

    return register_callback


# Renders a string into html and return the result. The `source` parameter is
# only used for reporting errors.
def render(text, ext, source=''):
    if ext in _callbacks:
        try:
            return _callbacks[ext](text)
        except Exception as err:
            msg =  f"Rendering Error: {source}\n"
            msg += f">> {err.__class__.__name__}: {err}"
            if (cause := err.__cause__):
                msg += f"\n>> Cause: {cause.__class__.__name__}: {cause}"
            elif (context := err.__context__):
                msg += f"\n>> Context: {context.__class__.__name__}: {context}"
            sys.exit(msg)
    return text


# Returns true if a rendering-engine callback has been registered for the
# specified file extension.
def is_registered_ext(ext):
    return ext in _callbacks
