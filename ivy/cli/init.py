# --------------------------------------------------------------------------
# Logic for the 'init' command.
# --------------------------------------------------------------------------

import os
import sys

from .. import utils


# Command help text.
helptext = """
Usage: %s init [FLAGS] [ARGUMENTS]

  Initialize a new site directory. If a directory path is specified, that
  directory will be created and initialized. Otherwise, the current directory
  will be initialized. Existing files will not be overwritten.

Arguments:
  [directory]         Directory name. Defaults to the current directory.

Flags:
  --help              Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Command callback.
def callback(parser):
    ivydir = os.path.dirname(os.path.dirname(__file__))
    inidir = os.path.join(ivydir, 'ini')
    dstdir = parser.get_args()[0] if parser.has_args() else '.'
    os.makedirs(dstdir, exist_ok=True)
    os.chdir(dstdir)

    for name in ('ext', 'inc', 'lib', 'out', 'res', 'src'):
        os.makedirs(name, exist_ok=True)

    utils.copydir(inidir, '.', noclobber=True)
