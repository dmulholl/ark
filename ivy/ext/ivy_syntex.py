# ------------------------------------------------------------------------------
# This extension adds support for source files in Syntex format. Syntex has
# been renamed Monk - this file is retained for backwards compatability. It
# will be removed in a future release.
# ------------------------------------------------------------------------------

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
