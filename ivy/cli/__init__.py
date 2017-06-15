# --------------------------------------------------------------------------
# This package processes the application's command-line arguments.
# --------------------------------------------------------------------------

import os
import sys

import clio
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
Usage: %s [FLAGS] [COMMAND]

  Ivy is a static website generator. It transforms a directory of text files
  into a self-contained website.

Flags:
  --help              Print the application's help text and exit.
  --version           Print the application's version number and exit.

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
    global parser

    # Root parser.
    parser = clio.ArgParser(helptext, ivy.__version__)

    # Register the 'build' command.
    cmd_build = parser.add_cmd("build", build.helptext, build.callback)
    cmd_build.add_flag("clear c")
    cmd_build.add_str("out o", None)
    cmd_build.add_str("src s", None)
    cmd_build.add_str("lib l", None)
    cmd_build.add_str("inc i", None)
    cmd_build.add_str("res r", None)
    cmd_build.add_str("theme t", None)

    # Register the 'clear' command.
    parser.add_cmd("clear", clear.helptext, clear.callback)

    # Register the 'init' command.
    parser.add_cmd("init", init.helptext, init.callback)

    # Register the 'serve' command.
    cmd_serve = parser.add_cmd("serve", serve.helptext, serve.callback)
    cmd_serve.add_flag("no-browser")
    cmd_serve.add_str("directory d", None)
    cmd_serve.add_str("host h", "localhost")
    cmd_serve.add_int("port p", 0)
    cmd_serve.add_str("b browser", None)

    # Register the 'watch' command.
    cmd_watch = parser.add_cmd("watch", watch.helptext, watch.callback)
    cmd_watch.add_flag("clear c")
    cmd_watch.add_str("out o", None)
    cmd_watch.add_str("src s", None)
    cmd_watch.add_str("lib l", None)
    cmd_watch.add_str("inc i", None)
    cmd_watch.add_str("res r", None)
    cmd_watch.add_str("theme t", None)

    # Fire the 'cli' event. Plugins can use this event to register their own
    # custom commands and options.
    ivy.hooks.event('cli', parser)

    # Parse the application's command line arguments.
    parser.parse()
