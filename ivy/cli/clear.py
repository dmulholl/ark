# --------------------------------------------------------------------------
# Logic for the 'clear' command.
# --------------------------------------------------------------------------

import sys
import os

from .. import site
from .. import utils


# Command help text.
helptext = """
Usage: %s clear [FLAGS]

  Clear the output directory.

Flags:
  --help              Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Command callback.
def callback(parser):
    if not site.home():
        sys.exit("Error: cannot locate the site's home directory.")

    if not os.path.exists(site.out()):
        sys.exit("Error: cannot locate the site's output directory.")

    utils.cleardir(site.out())
