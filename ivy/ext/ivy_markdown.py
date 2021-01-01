import ivy

try:
    import markdown
except ImportError:
    markdown = None

if markdown:

    # Check the config file for custom settings for the markdown renderer.
    # (The bare 'markdown' attribute is deprecated.)
    settings = ivy.site.config.get('markdown_settings') or ivy.site.config.get('markdown') or {}

    # Initialize a markdown renderer.
    renderer = markdown.Markdown(**settings)

    # Register a callback to render files with a .md extension.
    @ivy.renderers.register('md')
    def render(text):
        return renderer.reset().convert(text)
