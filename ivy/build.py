# ------------------------------------------------------------------------------
# This module contains the default build routine. It creates a single html page
# in the output directory for each node in the node tree.
# ------------------------------------------------------------------------------

import os
import sys

from . import events
from . import nodes
from . import site
from . import utils
from . import pages
from . import filters


# The `main_build` event is fired by the `$ ivy build` command.
@events.register('main_build')
def build_site():

    # Make sure we have a valid theme directory.
    if not site.theme():
        theme_name =  site.config['theme']
        sys.exit(f"Error: cannot locate theme '{theme_name}'.")

    # Copy the theme's resource files to the output directory.
    if os.path.isdir(site.theme('resources')):
        utils.copydir(site.theme('resources'), site.out())

    # Copy the site's resource files to the output directory.
    if os.path.exists(site.res()):
        utils.copydir(site.res(), site.out())

    # Callback to handle individual nodes.
    def build_node(node):
        if filters.apply('build_node', True, node):
            node.render()
            page = pages.Page(node)
            page.write()

    # Walk the node tree and pass each node to the handler.
    nodes.root().walk(build_node)

