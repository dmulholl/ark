# --------------------------------------------------------------------------
# Ivy: a static website generator.
#
# Author: Darren Mulholland <darren@mulholland.xyz>
# License: Public Domain
# --------------------------------------------------------------------------

import sys


# Application version number.
__version__ = '0.3.3'


# Ivy requires at least Python 3.5.
if sys.version_info < (3, 5):
    sys.exit('Error: Ivy requires Python >= 3.5.')


# Template for error messages informing the user of any missing dependencies.
error = """Error: Ivy requires the %s library. Try:

    $ pip install %s"""


# Check that the application's dependencies are available.
try:
    import clio
except ImportError:
    sys.exit(error % ('Clio', 'libclio'))


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


# The main() function provides the application's entry point. Calling main()
# initializes the site model, loads the site's plugins, and fires a series of
# event hooks. All the application's functionality is handled by callbacks
# registered on these hooks.
def main():

    # Initialize the site model.
    site.init()

    # Load plugins.
    extensions.load()

    # Process the application's command-line arguments.
    cli.parse()

    # Load the theme.
    theme.load()

    # Fire the 'init' event. (Runs callbacks registered on the 'init' hook.)
    hooks.event('init')

    # Fire the 'main' event. (Runs callbacks registered on the 'main' hook.)
    hooks.event('main')

    # Fire the 'exit' event. (Runs callbacks registered on the 'exit' hook.)
    hooks.event('exit')
