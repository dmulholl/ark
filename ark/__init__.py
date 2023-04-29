# ------------------------------------------------------------------------------
# Ark: a static website generator.
# ------------------------------------------------------------------------------

__version__ = '7.0.0'

import sys
if sys.version_info < (3, 10):
    sys.exit('Error: Ark requires Python 3.10 or later.')


# On Windows, use the 'colorama' package if it's available to support ANSI
# terminal codes.
if sys.platform == 'win32':
    try:
        import colorama
    except ImportError:
        pass
    else:
        colorama.init()


# We import the package's modules so users can access 'ark.foo' via a simple
# 'import ark' statement. Otherwise the user would have to import each module
# individually as 'import ark.foo'.
from . import cli
from . import extensions
from . import hashes
from . import events
from . import filters
from . import nodes
from . import renderers
from . import site
from . import utils


# Application entry point. Calling main() initializes the site model, loads
# the site's plugins, then fires a sequence of event hooks. All of Ark's
# functionality is handled by callbacks registered on these hooks.
def main():

    # Initialize the site model.
    site.init()

    # Load plugins bundled with Ark itself, then any plugins listed in the
    # site's config.py file, then any plugins in the site's 'ext' directory.
    extensions.load_bundled_extensions()
    extensions.load_installed_extensions()
    extensions.load_site_extensions()

    # Process the command-line arguments.
    cli.parse_args()

    # Load any plugins bundled with the active theme.
    extensions.load_theme_extensions()

    # Fire the primary sequence of event hooks.
    events.fire(events.Event.INIT)
    events.fire(events.Event.MAIN)
    events.fire(events.Event.EXIT)
