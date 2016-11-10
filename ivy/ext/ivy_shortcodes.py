# --------------------------------------------------------------------------
# This extension adds support for shortcodes.
# --------------------------------------------------------------------------

import ivy
import sys

try:
    import shortcodes
except ImportError:
    shortcodes = None


# The shortcodes package is an optional dependency.
if shortcodes:

    # Check the site's config file for customized settings for the shortcode
    # parser.
    settings = ivy.site.config.get('shortcodes', {})

    # Initialize a single parser instance.
    parser = shortcodes.Parser(**settings)

    # Filter each node's content on the 'node_text' filter hook and render
    # any shortcodes contained in it.
    @ivy.hooks.register('node_text')
    def render(text, node):
        try:
            return parser.parse(text, node)
        except shortcodes.ShortcodeError as err:
            msg =  "-------------------\n"
            msg += "  Shortcode Error  \n"
            msg += "-------------------\n\n"
            msg += "  Node: %s\n\n" % node.path()
            msg += "  %s: %s" % (err.__class__.__name__, err)
            if err.__context__:
                cause = err.__context__
                msg += "\n\n  The following cause was reported:\n\n"
                msg += "  %s: %s" % (cause.__class__.__name__, cause)
            sys.exit(msg)
