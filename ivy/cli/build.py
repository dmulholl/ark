# ------------------------------------------------------------------------------
# This module contains the logic for the 'build' command.
# ------------------------------------------------------------------------------

import os
import sys

from .. import site
from .. import events
from .. import utils


helptext = """
Usage: %s build

  Build the current site. This command can be run from the site directory or
  any of its subdirectories.

  The --theme option can be used to override the theme specified in the site's
  configuration file. It accepts either a theme name or an explicit path to a
  theme directory.

Options:
  -t, --theme <name>    Override the default theme.

Flags:
  -c, --clear           Clear the output directory before building.
  -h, --help            Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


@events.register('cli')
def register_command(parser):
    cmd = parser.command("build", helptext, cmd_callback)
    cmd.flag("clear c")
    cmd.option("theme t")


def cmd_callback(cmd_name, cmd_parser):
    if not site.home():
        sys.exit("Error: cannot locate the site's home directory.")
    if cmd_parser.found('theme'):
        site.config['theme'] = cmd_parser.value('theme')
    if cmd_parser.found('clear'):
        utils.cleardir(site.out())

    @events.register('main')
    def fire_build_events():
        events.fire('init_build')
        events.fire('main_build')
        events.fire('exit_build')

