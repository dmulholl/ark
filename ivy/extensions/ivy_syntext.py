##
## Add support for Syntext files with a `.stx` extension.
##

import ivy

try:
    import syntext
except ImportError:
    syntext = None

settings = ivy.site.config.get('syntext_settings') or {'pygmentize': True}

if syntext:
    @ivy.renderers.register('stx')
    def render_syntext(text):
        return syntext.render(text, **settings)
