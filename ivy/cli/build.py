# ------------------------------------------------------------------------------
# This module contains the logic for the 'build' command.
# ------------------------------------------------------------------------------

import os
import sys
import datetime

from .. import site
from .. import events
from .. import utils
from .. import nodes
from .. import filters
from .. import hashes


helptext = """
Usage: ivy build

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
"""


@events.register(events.Event.CLI)
def register_command(argparser):
    cmd_parser = argparser.command("build", helptext, cmd_callback)
    cmd_parser.flag("clear c")
    cmd_parser.option("theme t")


def cmd_callback(cmd_name, cmd_parser):
    if not site.home():
        sys.exit("Error: cannot locate the site's home directory.")
    if cmd_parser.found('theme'):
        site.config['theme'] = cmd_parser.value('theme')
    if cmd_parser.found('clear'):
        utils.cleardir(site.out())
        hashes.clear()

    @events.register(events.Event.MAIN)
    def fire_build_events():
        events.fire(events.Event.INIT_BUILD)
        events.fire(events.Event.MAIN_BUILD)
        events.fire(events.Event.EXIT_BUILD)


@events.register(events.Event.MAIN_BUILD)
def build_site():
    # Make sure we have a valid theme directory.
    if not site.theme():
        theme_name = site.config['theme']
        sys.exit(f"Error: cannot locate the theme '{theme_name}'.")

    # Copy the theme's resource files to the output directory.
    if os.path.isdir(site.theme('resources')):
        utils.copydir(site.theme('resources'), site.out())

    # Copy the site's resource files to the output directory.
    if os.path.exists(site.res()):
        utils.copydir(site.res(), site.out())

    # Callback to handle individual nodes. The `build_node` filter can be used
    # as a switch to decide if a node should be written to disk. A `disable`
    # flag in a node's metadata header will also prevent Ivy from producing an
    # output HTML page for a node.
    def build_node(node):
        if filters.apply('build_node', True, node) and not node.get('disable'):
            node.write()

    # Walk the node tree and pass each node to the handler.
    nodes.root().walk(build_node)


@events.register(events.Event.EXIT_BUILD)
def print_build_stats():
    report = datetime.datetime.now().strftime("[%H:%M:%S]")
    report += f"   ·   Rendered: {site.pages_rendered():5d}"
    report += f"   ·   Written: {site.pages_written():5d}"
    report += f"   ·   Time: {site.runtime():6.2f} sec"
    report = report.replace('·', '\u001B[90m·\u001B[0m')
    utils.safeprint(report)
