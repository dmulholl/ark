# ------------------------------------------------------------------------------
# Ivy: a static website generator.
# ------------------------------------------------------------------------------

__version__ = '3.1.0'

import sys
if sys.version_info < (3, 8):
    sys.exit('Error: Ivy requires Python 3.8 or later.')


# On Windows, use colorama to support ANSI terminal codes.
if sys.platform == 'win32':
    try:
        import colorama
    except ImportError:
        pass
    else:
        colorama.init()


# We import the package's modules so users can access 'ivy.foo' via a simple
# 'import ivy' statement. Otherwise the user would have to import each module
# individually as 'import ivy.foo'.
from . import cli
from . import extensions
from . import hashes
from . import events
from . import filters
from . import nodes
from . import pages
from . import renderers
from . import site
from . import utils


# Application entry point. Calling main() initializes the site model, loads
# the site's plugins, then fires a sequence of event hooks. All of Ivy's
# functionality is handled by callbacks registered on these hooks.
def main():

    # Initialize the site model.
    site.init()

    # Load bundled plugins, plugins listed in the site's configuration file,
    # and plugins in the site's 'ext' directory.
    extensions.load_bundled_extensions()
    extensions.load_installed_extensions()
    extensions.load_site_extensions()

    # Process the application's command-line arguments.
    cli.parse_args()

    # Load any plugins bundled with the active theme.
    extensions.load_theme_extensions()

    # Fire the primary sequence of event hooks.
    events.fire('init')
    events.fire('main')
    events.fire('exit')
