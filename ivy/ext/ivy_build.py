# --------------------------------------------------------------------------
# Default build routine. Builds a page for each node in the parse tree.
# --------------------------------------------------------------------------

import os
import sys

from ivy import hooks, site, utils, nodes, pages


# Register our build callback on the 'main_build' event hook.
@hooks.register('main_build')
def build_site():

    # Make sure we have a valid theme directory.
    if not site.theme():
        sys.exit("Error: cannot locate theme '%s'." % site.config['theme'])

    # Copy the theme's resource files to the output directory.
    if os.path.isdir(site.theme('resources')):
        utils.copydir(site.theme('resources'), site.out())

    # Copy the site's resource files to the output directory.
    if os.path.exists(site.res()):
        utils.copydir(site.res(), site.out())

    # Walk the parse tree and render a page for each node.
    nodes.root().walk(lambda node: pages.Page(node).render())
