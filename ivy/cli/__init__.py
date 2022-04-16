# ------------------------------------------------------------------------------
# This package processes the application's command-line arguments.
# ------------------------------------------------------------------------------

import ivy
import sys
import argslib

from . import build
from . import init
from . import clear
from . import serve
from . import watch
from . import add
from . import tree
from . import open
from . import deploy


helptext = f"""
Ivy v{ivy.__version__}

  Ivy is a static website generator. It transforms a directory of text files
  into a self-contained website.

Usage:
  ivy <flag>
  ivy <command>
  ivy help <command>

Flags:
  -h, --help          Print the application's help text and exit.
  -v, --version       Print the application's version number and exit.

Commands:
  add                 Add a new node file.
  build               Build the site.
  clear               Clear the output directory.
  deploy              Deploy the site.
  init                Initialize a new site directory.
  open                Open an @root/ url in the default web browser.
  serve               Run the test server on the site's output directory.
  tree                Print the node tree.
  watch               Monitor the site directory and rebuild on changes.

Command Help:
  help <command>      Print the specified command's help text and exit.
"""


# We store the root ArgParser instance globally so it's available to plugins.
argparser = argslib.ArgParser(helptext, ivy.__version__)


# Parse the application's command-line arguments. Plugins can use the `CLI`
# event to register their own custom commands.
def parse_args():
    ivy.events.fire(ivy.events.Event.CLI, argparser)
    argparser.parse()

    if argparser.command_name is None:
        print(helptext.strip())
        sys.exit()
