# Add support for Syntext files with a `.stx` extension.

import ark

try:
    import syntext
except ImportError:
    syntext = None

settings = ark.site.config.get('syntext_settings') or {'pygmentize': True}

if syntext:
    @ark.renderers.register('stx')
    def render_syntext(text):
        return syntext.render(text, **settings)
