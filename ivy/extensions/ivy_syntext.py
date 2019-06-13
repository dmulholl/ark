# ------------------------------------------------------------------------------
# This extension adds support for source files in Syntext format.
# ------------------------------------------------------------------------------

import ivy

try:
    import syntext
except ImportError:
    syntext = None


# The syntext package is an optional dependency. 
if syntext:
    @ivy.renderers.register('stx')
    def render(text):
        return syntext.render(text, pygmentize=True)
