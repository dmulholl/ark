##
## Add support for Markdown files with a `.md` extension.
##

import ivy

try:
    import markdown
except ImportError:
    markdown = None

if markdown:
    settings = ivy.site.config.get('markdown_settings') or {}
    renderer = markdown.Markdown(**settings)

    @ivy.renderers.register('md')
    def render_markdown(text):
        return renderer.reset().convert(text)
