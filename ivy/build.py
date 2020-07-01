# ------------------------------------------------------------------------------
# This module contains the default build routine. It creates a single html page
# in the output directory for each node in the parse tree.
# ------------------------------------------------------------------------------

import os
import sys

from . import events
from . import nodes
from . import site
from . import utils
from . import pages


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

    # Callback to render a single node instance.
    def render(node):
        pages.Page(node).render()

    # Walk the parse tree and pass each node to the render callback.
    nodes.root().walk(render)

