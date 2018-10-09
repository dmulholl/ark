# ------------------------------------------------------------------------------
# This package processes the application's command-line arguments.
# ------------------------------------------------------------------------------

import os
import sys

import janus
import ivy

from . import build
from . import init
from . import clear
from . import serve
from . import watch


# We want the root ArgParser instance to be available to plugins.
parser = None


# Application help text.
helptext = """
Usage: %s [command]

  Ivy is a static website generator. It transforms a directory of text files
  into a self-contained website.

Flags:
  -h, --help          Print the application's help text and exit.
  -v, --version       Print the application's version number and exit.

Commands:
  build               Build the site.
  clear               Clear the output directory.
  init                Initialize a new site directory.
  serve               Run a web server on the site's output directory.
  tree                Print the site's node tree.
  watch               Monitor the site directory and rebuild on changes.

Command Help:
  help <command>      Print the specified command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Parse the application's command-line arguments.
def parse():

    # We make the root parser global so plugins can inspect it.
    global parser
    parser = janus.ArgParser(helptext, ivy.__version__)

    # Fire the 'cli' event. Plugins can use this event to register their own
    # custom commands and options.
    ivy.hooks.event('cli', parser)

    # Parse the application's command line arguments.
    parser.parse()
    if not parser.has_cmd():
        parser.exit_help()
