##
## Add support for Syntext files with a `.stx` extension.
##

import ivy

try:
    import syntext
except ImportError:
    syntext = None

if syntext:
    @ivy.renderers.register('stx')
    def render_syntext(text):
        return syntext.render(text, pygmentize=True)
