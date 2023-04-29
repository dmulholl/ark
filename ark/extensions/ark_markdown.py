# Add support for Markdown files with a `.md` extension.

import ark

try:
    import markdown
except ImportError:
    markdown = None

if markdown:
    settings = ark.site.config.get('markdown_settings') or {}
    renderer = markdown.Markdown(**settings)

    @ark.renderers.register('md')
    def render_markdown(text):
        return renderer.reset().convert(text)
