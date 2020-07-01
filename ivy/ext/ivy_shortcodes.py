# ------------------------------------------------------------------------------
# This extension adds support for shortcodes.
# ------------------------------------------------------------------------------

import ivy
import sys

try:
    import shortcodes
except ImportError:
    shortcodes = None


# Check the config file for custom settings for the shortcode parser.
settings = ivy.site.config.get('shortcodes', {})


# The shortcodes module is an optional dependency.
if shortcodes:

    # Initialize a single parser instance.
    parser = shortcodes.Parser(**settings)

    # Filter each node's content on the 'node_text' filter hook.
    @ivy.filters.register('node_text')
    def render(text, node):
        try:
            return parser.parse(text, node)
        except shortcodes.ShortcodeError as err:
            msg = "Shortcode Error\n"
            msg += f"  Node: {node}\n"
            msg += f"  {err.__class__.__name__}: {err}"
            if (cause := err.__context__):
                msg += f"\n  Cause: {cause.__class__.__name__}: {cause}"
            sys.exit(msg)
