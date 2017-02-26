# --------------------------------------------------------------------------
# Default site building routine. Builds a page or leaf index for each node
# in the parse tree.
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

    # Run the build_node callback on each node in the parse tree.
    nodes.root().walk(build_node)


# This function will be called on each node in the parse tree.
def build_node(node):
    pages.Page(node).render()
