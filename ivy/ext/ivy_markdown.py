##
# This extension adds support for Markdown files with a `.md` extension.
##

import ivy

try:
    import markdown
except ImportError:
    markdown = None

if markdown:

    # Check the config file for custom settings for the markdown renderer.
    settings = ivy.site.config.get('markdown_settings') or {}

    # Initialize a markdown renderer.
    renderer = markdown.Markdown(**settings)

    # Register a callback to render files with a .md extension.
    @ivy.renderers.register('md')
    def render(text):
        return renderer.reset().convert(text)
