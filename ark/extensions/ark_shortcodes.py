# Add support for shortcodes in node content.

import ark
import sys

try:
    import shortcodes
except ImportError:
    shortcodes = None


# We parse all shortcodes using this single Parser instance.
parser = None


# The shortcodes package is an optional dependency.
if shortcodes:

    # We process and replace shortcodes in the node's text content just before
    # that text is rendered into HTML.
    @ark.filters.register(ark.filters.Filter.NODE_TEXT)
    def render_shortcodes(text, node):
        global parser
        if parser is None:
            settings = ark.site.config.get('shortcode_settings') or {}
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
