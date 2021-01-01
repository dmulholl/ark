import ivy
import sys

try:
    import shortcodes
except ImportError:
    shortcodes = None


# Use a single parser instance to parse all files.
parser = None


# The bare 'shortcodes' attribute for custom settings is deprecated.
if shortcodes:

    @ivy.filters.register('node_text')
    def render(text, node):
        global parser
        if parser is None:
            new_settings = ivy.site.config.get('shortcode_settings')
            old_settings = ivy.site.config.get('shortcodes')
            settings = new_settings or old_settings or {}
            parser = shortcodes.Parser(**settings)

        try:
            return parser.parse(text, node)
        except shortcodes.ShortcodeError as err:
            msg = "Shortcode Error\n"
            msg += f">> Node: {node.url}\n"
            msg += f">> {err.__class__.__name__}: {err}"
            if (cause := err.__cause__):
                msg += f"\n>> Cause: {cause.__class__.__name__}: {cause}"
            sys.exit(msg)
