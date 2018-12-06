# ------------------------------------------------------------------------------
# Ivy: a static website generator.
#
# Author: Darren Mulholland <dmulholl@tcd.ie>
# License: Public Domain
# ------------------------------------------------------------------------------

import sys


# Application version number.
__version__ = '2.0.2'


# Ivy requires at least Python 3.6.
if sys.version_info < (3, 6):
    sys.exit('Error: Ivy requires Python 3.6 or later.')


# Template for error messages informing the user of any missing dependencies.
errorstr = """Error: Ivy requires the %s library. Try:

    $ pip install %s"""


# Check that the application's dependencies are available.
try:
    import janus
except ImportError:
    sys.exit(errorstr % ('Janus', 'libjanus'))
try:
    import shortcodes
except ImportError:
    sys.exit(errorstr % ('Shortcodes', 'shortcodes'))


# We import the package's modules so users can access 'ivy.foo' via a simple
# 'import ivy' statement. Otherwise the user would have to import each module
# individually as 'import ivy.foo'.
from . import cli
from . import extensions
from . import hashes
from . import hooks
from . import includes
from . import loader
from . import nodes
from . import pages
from . import renderers
from . import site
from . import theme


# Application entry point. Calling main() initializes the site model, loads
# the site's plugins, and fires a sequence of event hooks. All of Ivy's
# functionality is handled by callbacks registered on these hooks.
def main():

    # Initialize the site model.
    site.init()

    # Load bundled plugins, plugins in the site extensions directory, and
    # plugins listed in the site configuration file.
    extensions.load()

    # Process the application's command-line arguments.
    cli.parse()

    # Load any plugins bundled with the active theme.
    theme.load()

    # Fire the sequence of event hooks.
    hooks.event('init')
    hooks.event('main')
    hooks.event('exit')
