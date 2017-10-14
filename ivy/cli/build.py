# ------------------------------------------------------------------------------
# This module contains the logic for the 'build' command.
# ------------------------------------------------------------------------------

import os
import sys

from .. import site
from .. import hooks
from .. import nodes
from .. import pages
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
  -h, --help            Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Register the command on the 'cli' event hook.
@hooks.register('cli')
def register_command(parser):
    cmd = parser.new_cmd("build", helptext, callback)
    cmd.new_flag("clear c")
    cmd.new_str("out o")
    cmd.new_str("src s")
    cmd.new_str("lib l")
    cmd.new_str("inc i")
    cmd.new_str("res r")
    cmd.new_str("theme t")


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


# Default build routine. Creates a single output page for each node in the
# parse tree.
@hooks.register('main_build')
def builder():

    # Make sure we have a valid theme directory.
    if not site.theme():
        sys.exit("Error: cannot locate theme '%s'." % site.config['theme'])

    # Copy the theme's resource files to the output directory.
    if os.path.isdir(site.theme('resources')):
        utils.copydir(site.theme('resources'), site.out())

    # Copy the site's resource files to the output directory.
    if os.path.exists(site.res()):
        utils.copydir(site.res(), site.out())

    # Walk the parse tree and render a single page for each node.
    nodes.root().walk(lambda node: pages.Page(node).render())
