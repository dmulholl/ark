# ------------------------------------------------------------------------------
# This extension adds a 'tree' command to Ivy's command line interface. We
# implement the command here rather than in the cli package to provide an
# example of an extension registering a custom command.
# ------------------------------------------------------------------------------

import ivy
import sys
import os


# Command help text.
helptext = """
Usage: %s tree [FLAGS]

  Print the site's node tree. The root node to use as the starting point can
  be determined by specifying its url, e.g.

    $ ivy tree --root @root/foo/bar//

Options:
  -r, --root <url>      Specify the root node. (Defaults to the site root.)

Flags:
  -h, --help            Print this command's help text and exit.
  -s, --slugs           Show slugs instead of urls.

""" % os.path.basename(sys.argv[0])


# Register our command on the 'cli' event hook.
@ivy.events.register('cli')
def register_command(parser):
    cmd_parser = parser.command("tree", helptext, cmd_callback)
    cmd_parser.flag("slugs s")
    cmd_parser.option("root r", default="@root/")


# Command callback. This function will be called by the command-line parser if
# the 'tree' command is found. We can't print the tree until the site model has
# been fully initialized so we register a callback to fire after initialization.
def cmd_callback(cmd_name, cmd_parser):
    show_urls = False if cmd_parser.found("slugs") else True
    root_url = cmd_parser.value("root")

    @ivy.events.register('main')
    def tree_callback():
        if not ivy.site.home():
            sys.exit("Error: cannot locate the site's home directory.")
        if (node := ivy.nodes.node(root_url)) is None:
            sys.exit("Error: cannot find the specified root node.")
        ivy.utils.termline()
        ivy.utils.safeprint('Site: %s' % ivy.site.home())
        ivy.utils.termline()
        ivy.utils.safeprint(node.tree(urls=show_urls))
        ivy.utils.termline()

