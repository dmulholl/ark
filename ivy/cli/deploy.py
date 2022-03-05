# ------------------------------------------------------------------------------
# This module contains the logic for the 'deploy' command.
# ------------------------------------------------------------------------------

import os
import sys

from .. import site
from .. import events


helptext = """
Usage: ivy deploy

  This command fires an 'Event.DEPLOY' event hook which plugins can use to
  run site deployment scripts.

  Alternatively, you can add a 'deploy_script' attribute to your site's
  configuration file, e.g.

    deploy_script = "bin/deploy.sh"

  This command will run the referenced script. The script's path should be
  specified relative to the site's home directory.

Flags:
  -h, --help            Print this command's help text and exit.
"""


@events.register(events.Event.CLI)
def register_command(argparser):
    argparser.command("deploy", helptext, cmd_callback)


def cmd_callback(cmd_name, cmd_parser):
    if not site.home():
        sys.exit("Error: cannot locate the site's home directory.")
    if not os.path.isdir(site.out()):
        sys.exit("Error: cannot locate the site's output directory.")

    if (script := site.config.get("deploy_script")):
        path = os.path.join(site.home(), script)
        os.system(path)

    @events.register(events.Event.MAIN)
    def fire_deploy_event():
        events.fire(events.Event.DEPLOY)
