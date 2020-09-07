# ------------------------------------------------------------------------------
# This module contains the logic for the 'tree' command.
# ------------------------------------------------------------------------------

import os
import sys

from .. import site
from .. import nodes
from .. import utils
from .. import events


helptext = """
Usage: %s tree

  This command prints the site's node tree. The root note to use as the
  starting point can be specifed using the --root option:

    $ ivy tree --root @root/foo/bar//

  The tree displays urls by default. Use the --slugs flag to print slugs
  instead. Use the --attr option to append the value of an arbitrary attribute,
  e.g.

    $ ivy tree --attr title --attr date

Options:
  -a, --attr <name>     Attribute to display.
  -r, --root <url>      Specify the root node. (Defaults to the site root.)

Flags:
  -h, --help            Print this command's help text and exit.
  -s, --slugs           Show slugs instead of urls.

""" % os.path.basename(sys.argv[0])


@events.register('cli')
def register_command(argparser):
    cmd_parser = argparser.command("tree", helptext, cmd_callback)
    cmd_parser.flag("slugs s")
    cmd_parser.option("root r", default="@root/")
    cmd_parser.option("attr a")


def cmd_callback(cmd_name, cmd_parser):
    base = 'slug' if cmd_parser.found('slugs') else 'url'

    @events.register('main')
    def tree_callback():
        if not site.home():
            sys.exit("Error: cannot locate the site's home directory.")
        if (node := nodes.node(cmd_parser.value("root"))) is None:
            sys.exit("Error: cannot find the specified root node.")
        utils.termline()
        utils.safeprint('Site: %s' % site.home())
        utils.termline()
        utils.safeprint(treestring(node, depth=0, base=base, attrs=cmd_parser.values('attr')))
        utils.termline()


def treestring(node, depth, base, attrs):
    if base == 'url':
        line = '·  ' * depth + node.url
    else:
        line = '·  ' * depth + node.slug or '/'
    for attr in attrs:
        line += '  \u001B[90m--\u001B[0m  ' + repr(node.get(attr))
    lines = [line]
    for child in sorted(node.children, key=lambda node: node.slug):
        lines.append(treestring(child, depth + 1, base, attrs))
    return '\n'.join(lines)
