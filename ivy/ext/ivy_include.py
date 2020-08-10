# ------------------------------------------------------------------------------
# This is a sample shortcode plugin. It registers an [% include %] shortcode
# that you can use to inject the content of files from your site's 'inc'
# directory directly into node files.
#
# To use it, just supply the name of the file you want to include:
#
#   [% include file.md %]
#
# Note that shortcodes are processed *before* a node's text is rendered into
# HTML so the format of the included file should be compatible with the format
# of the rest of the node's content (e.g. if the node's content is written in
# Markdown then the included content should also be in Markdown or HTML).
# ------------------------------------------------------------------------------

import os
import ivy

try:
    import shortcodes
except ImportError:
    shortcodes = None


# The shortcodes module is an optional dependency so we check that it's actually
# installed before trying to use it.
if shortcodes:

    @shortcodes.register('include')
    def handler(node, content, pargs, kwargs):
        if pargs:
            path = ivy.site.inc(pargs[0])
            if os.path.exists(path):
                with open(path) as file:
                    return file.read()
        return ''
