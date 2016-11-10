# --------------------------------------------------------------------------
# This extension adds support for source files in Syntex format. Files with
# a .stx extension will be rendered as Syntex.
# --------------------------------------------------------------------------

import ivy

try:
    import syntex
except ImportError:
    syntex = None


# The syntex package is an optional dependency.
if syntex:

    # Register a callback to render files with a .stx extension.
    @ivy.renderers.register('stx')
    def render(text):
        return syntex.render(text, pygmentize=True)
