# ------------------------------------------------------------------------------
# This extension adds support for source files in Monk format.
# ------------------------------------------------------------------------------

import ivy

try:
    import monk

    @ivy.renderers.register('mk')
    @ivy.renderers.register('monk')
    def render(text):
        return monk.render(text, pygmentize=True)

except ImportError:
    pass
