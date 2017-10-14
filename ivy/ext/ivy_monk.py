# ------------------------------------------------------------------------------
# This extension adds support for source files in Monk format.
# ------------------------------------------------------------------------------

import ivy

try:
    import monk
except ImportError:
    monk = None


# The monk package is an optional dependency.
if monk:

    # Register a callback to render files with a .mk or .monk extension.
    @ivy.renderers.register('mk')
    @ivy.renderers.register('monk')
    def render(text):
        return monk.render(text, pygmentize=True)
