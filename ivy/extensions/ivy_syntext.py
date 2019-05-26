# ------------------------------------------------------------------------------
# This extension adds support for source files in Syntext format.
# ------------------------------------------------------------------------------

import ivy

try:
    import syntext
except ImportError:
    syntext = None


# The syntext package is an optional dependency. We keep the bindings to .mk
# .monk for backwards compatibility.
if syntext:
    @ivy.renderers.register('stx', 'mk', 'monk')
    def render(text):
        return syntext.render(text, pygmentize=True)
