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
    @ivy.renderers.register('mk', 'monk')
    def render(text):
        return monk.render(text, pygmentize=True)
