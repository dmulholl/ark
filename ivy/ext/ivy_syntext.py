##
# This extension adds support for Syntext files with a `.stx` extension.
##

import ivy

try:
    import syntext
except ImportError:
    pass
else:
    @ivy.renderers.register('stx')
    def render(text):
        return syntext.render(text, pygmentize=True)
