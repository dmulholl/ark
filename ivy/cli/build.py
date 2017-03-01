# --------------------------------------------------------------------------
# Logic for the 'build' command.
# --------------------------------------------------------------------------

import os
import sys

from .. import site
from .. import hooks
from .. import utils


# Command help text.
helptext = """
Usage: %s build [FLAGS] [OPTIONS]

  Build the current site. This command can be run from the site directory or
  any of its subdirectories.

  The --theme option can be used to override the theme specified in the site's
  configuration file. It accepts either a theme name or an explicit path to a
  theme directory.

Options:
  -i, --inc <path>      Override the default 'inc' directory.
  -l, --lib <path>      Override the default 'lib' directory.
  -o, --out <path>      Override the default 'out' directory.
  -r, --res <path>      Override the default 'res' directory.
  -s, --src <path>      Override the default 'src' directory.
  -t, --theme <name>    Override the default theme.

Flags:
  -c, --clear           Clear the output directory before building.
      --help            Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Command callback.
def callback(parser):
    if not site.home():
        sys.exit("Error: cannot locate the site's home directory.")

    if parser['out']: site.cache['out'] = parser['out']
    if parser['src']: site.cache['src'] = parser['src']
    if parser['lib']: site.cache['lib'] = parser['lib']
    if parser['inc']: site.cache['inc'] = parser['inc']
    if parser['res']: site.cache['res'] = parser['res']

    if parser['theme']:
        site.config['theme'] = parser['theme']

    if parser['clear']:
        utils.cleardir(site.out())

    @hooks.register('main')
    def build_callback():
        hooks.event('init_build')
        hooks.event('main_build')
        hooks.event('exit_build')
