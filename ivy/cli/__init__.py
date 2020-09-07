# ------------------------------------------------------------------------------
# This package processes the application's command-line arguments.
# ------------------------------------------------------------------------------

import os
import sys
import args
import ivy

from . import build
from . import init
from . import clear
from . import serve
from . import watch
from . import make
from . import tree


helptext = """
Usage: %s [flag] [command]

  Ivy is a static website generator. It transforms a directory of text files
  into a self-contained website.

Flags:
  -h, --help          Print the application's help text and exit.
  -v, --version       Print the application's version number and exit.

Commands:
  build               Build the site.
  clear               Clear the output directory.
  init                Initialize a new site directory.
  make                Create a new node file.
  serve               Run a web server on the site's output directory.
  tree                Print the node tree.
  watch               Monitor the site directory and rebuild on changes.

Command Help:
  help <command>      Print the specified command's help text and exit.

""" % os.path.basename(sys.argv[0])


# We store the root ArgParser instance globally so it's available to plugins.
argparser = args.ArgParser(helptext, ivy.__version__)


# Parse the application's command-line arguments. Plugins can use the `cli`
# event to register their own custom commands.
def parse_args():
    ivy.events.fire('cli', argparser)
    argparser.parse()
