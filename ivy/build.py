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


# The `main_build` event is fired by the `$ ivy build` command. (It's one of
# three build events: `init_build`, `main_build`, `exit_build`.)
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
    def handle_node(node):
        node.render()
        page = pages.Page(node)
        page.write()

    # Walk the node tree and pass each node to the handler.
    nodes.root().walk(handle_node)

