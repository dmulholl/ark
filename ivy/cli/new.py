# ------------------------------------------------------------------------------
# This module contains the logic for the 'new' command.
# ------------------------------------------------------------------------------

import os
import sys
import datetime

from .. import utils
from .. import events
from .. import site


helptext = """
Usage: %s new <filename>

  Creates a new node file in the src directory. The filepath should be
  specified relative to the src directory. Creates directories along the
  path if required.

Arguments:
  <filepath>            File to create.

Options:
  -t, --title <str>     Specify a title string for the node.
  -d, --date <str>      Specify a date string for the node.

Flags:
  -f, --force           Overwrite an existing node file.
  -h, --help            Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


template = """\
---
title: {title}
date: {date}
---

"""


@events.register('cli')
def register_command(parser):
    cmd_parser = parser.command("new", helptext, cmd_callback)
    cmd_parser.option("title t")
    cmd_parser.option("date d")
    cmd_parser.flag("force f")


def cmd_callback(cmd_name, cmd_parser):
    if len(cmd_parser.args) == 0:
        sys.exit("Error: missing filepath.")

    filepath = site.src(cmd_parser.args[0])
    if os.path.exists(filepath) and not cmd_parser.found("force"):
        sys.exit(f"Error: the file '{filepath}' already exists.")

    values = {
        'title': cmd_parser.value('title') or "Untitled",
        'date': cmd_parser.value('date') or datetime.date.today()
    }
    utils.writefile(filepath, template.format(**values))
