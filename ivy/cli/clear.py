# ------------------------------------------------------------------------------
# This module contains the logic for the 'clear' command.
# ------------------------------------------------------------------------------

import sys
import os

from .. import site
from .. import utils
from .. import hooks


# Command help text.
helptext = """
Usage: %s clear

  Clear the output directory.

Flags:
  -h, --help          Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Register the command on the 'cli' event hook.
@hooks.register('cli')
def register_command(parser):
    parser.new_cmd("clear", helptext, callback)


# Command callback.
def callback(parser):
    if not site.home():
        sys.exit("Error: cannot locate the site's home directory.")

    if not os.path.exists(site.out()):
        sys.exit("Error: cannot locate the site's output directory.")

    utils.cleardir(site.out())
