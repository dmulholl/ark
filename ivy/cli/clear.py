# ------------------------------------------------------------------------------
# This module contains the logic for the 'clear' command.
# ------------------------------------------------------------------------------

import sys
import os

from .. import site
from .. import utils
from .. import events
from .. import hashes


helptext = """
Usage: ivy clear

  Clear the output directory.

Flags:
  -h, --help          Print this command's help text and exit.
"""


@events.register(events.Event.CLI)
def register_command(argparser):
    argparser.command("clear", helptext, cmd_callback)


def cmd_callback(cmd_name, cmd_parser):
    if not site.home():
        sys.exit("Error: cannot locate the site's home directory.")
    if not os.path.exists(site.out()):
        sys.exit("Error: cannot locate the site's output directory.")
    utils.cleardir(site.out())
    hashes.clear()
