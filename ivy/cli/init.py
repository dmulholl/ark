# ------------------------------------------------------------------------------
# This module contains the logic for the 'init' command.
# ------------------------------------------------------------------------------

import os
import sys

from .. import utils
from .. import events


helptext = """
Usage: %s init [directory]

  Initialize a new site directory. If a directory path is specified, that
  directory will be created and initialized. Otherwise, the current directory
  will be initialized. Existing files will not be overwritten.

Arguments:
  [directory]         Directory name. Defaults to the current directory.

Flags:
  -h, --help          Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


@events.register('cli')
def register_command(argparser):
    argparser.command("init", helptext, cmd_callback)


def cmd_callback(cmd_name, cmd_parser):
    ivy_dir = os.path.dirname(os.path.dirname(__file__))
    src_dir = os.path.join(ivy_dir, 'ini')
    dst_dir = cmd_parser.args[0] if cmd_parser.args else '.'
    os.makedirs(dst_dir, exist_ok=True)
    os.chdir(dst_dir)
    for name in ('inc', 'lib', 'src'):
        os.makedirs(name, exist_ok=True)
    utils.copydir(src_dir, '.', noclobber=True)
