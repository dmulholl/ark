# ------------------------------------------------------------------------------
# This module contains the logic for the 'add' command.
# ------------------------------------------------------------------------------

import os
import sys
import datetime

from .. import utils
from .. import events
from .. import site


helptext = """
Usage: ivy add <filename>

  This convenience command creates a new node file in the 'src' directory.
  The filename should be specified relative to the 'src' directory.
  Directories along the path will be created if required.

Arguments:
  <filename>            File to create.

Options:
  -t, --title <str>     Specify a title string for the node.
  -d, --date <str>      Specify a date string for the node.

Flags:
  -c, --content         Add dummy content.
  -f, --force           Overwrite an existing node file.
  -h, --help            Print this command's help text and exit.
"""


template1 = """\
---
title: {title}
date: {date}
---

"""


template2 = """\
---
title: {title}
date: {date}
---

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.

Brigantes femina duce exurere coloniam, expugnare castra, ac nisi felicitas in
tali casu effugium subveniebat in aperta et solida. Neque is miseriarum finis.
Struendum vallum, petendus agger, amissa magna ex parte luxus egestatis scelerum
sibi conscios nisi pollutum obstrictumque meritis suis principem passuros.
"""


@events.register(events.Event.CLI)
def register_command(argparser):
    cmd_parser = argparser.command("add", helptext, cmd_callback)
    cmd_parser.option("title t")
    cmd_parser.option("date d")
    cmd_parser.flag("force f")
    cmd_parser.flag("content c")


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

    if cmd_parser.found("content"):
        utils.writefile(filepath, template2.format(**values))
    else:
        utils.writefile(filepath, template1.format(**values))
