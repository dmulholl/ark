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

  Print the site's node tree.

Flags:
  -h, --help            Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Register our command on the 'cli' event hook.
@ivy.hooks.register('cli')
def register_command(parser):
    parser.new_cmd("tree", helptext, callback)


# Command callback. This function will be called by the command-line parser if
# the 'tree' command is found.
def callback(parser):

    # We can't print the tree until the site model has been fully initialized
    # so we register a callback to fire after initialization.
    @ivy.hooks.register('main')
    def tree_callback():
        if not ivy.site.home():
            sys.exit("Error: cannot locate the site's home directory.")
        ivy.utils.termline()
        ivy.utils.safeprint('Site: %s' % ivy.site.home())
        ivy.utils.termline()
        ivy.utils.safeprint(ivy.nodes.root().str())
        ivy.utils.termline()
