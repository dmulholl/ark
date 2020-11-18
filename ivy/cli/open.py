# ------------------------------------------------------------------------------
# This module contains the logic for the 'open' command.
# ------------------------------------------------------------------------------

import ivy
import sys
import webbrowser


helptext = """
Usage: ivy open [url]

  This command opens the output file corresponding to the specified @root/ url
  directly in the default web browser. Defaults to opening the site root if no
  url is specified.

Arguments:
  [url]             The @root/ url to open. Defaults to the site root.

Flags:
  -h, --help        Print this command's help text and exit.
"""


@ivy.events.register('cli')
def register_command(argparser):
    argparser.command("open", helptext, cmd_callback)


def cmd_callback(cmd_name, cmd_parser):
    arg = cmd_parser.args[0] if cmd_parser.args else "@root/"
    if (node := ivy.nodes.node(arg)):
        url  = "file://" + ivy.pages.Page(node).get_filepath()
        webbrowser.open(url)
    else:
        sys.exit(f"Error: unknown url '{arg}'.")

