# --------------------------------------------------------------------------
# This extension adds a 'tree' command to Ivy's command line interface. We
# implement the command here rather than in the cli package to provide an
# example of an extension registering a custom command.
# --------------------------------------------------------------------------

import ivy
import sys
import shutil
import os


# Command help text.
helptext = """
Usage: %s tree [FLAGS]

  Print the site's node tree.

Flags:
  --help                Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Register our command on the 'cli' event hook.
@ivy.hooks.register('cli')
def register_command(parser):
    parser.new_cmd("tree", helptext, callback)


# Command callback.
def callback(parser):

    @ivy.hooks.register('main')
    def tree_callback():
        if not ivy.site.home():
            sys.exit("Error: cannot locate the site's home directory.")

        cols, _ = shutil.get_terminal_size()

        print('─' * cols)
        print('Site: %s' % ivy.site.home())
        print('─' * cols)
        print(ivy.nodes.root().str())
        print('─' * cols)
