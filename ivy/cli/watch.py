# ------------------------------------------------------------------------------
# This module contains the logic for the 'watch' command.
# ------------------------------------------------------------------------------

import sys
import os
import hashlib
import time
import subprocess
import hashlib

from .. import site
from .. import utils
from .. import events


helptext = """
Usage: ivy watch

  Monitor the site directory and automatically rebuild the site when file
  changes are detected.

  The test server is automatically launched to view the site.

Options:
  -p, --port <int>      Port number to serve on. Defaults to 8080.
  -t, --theme <name>    Override the default theme.

Flags:
  -c, --clear           Clear the output directory before each build.
  -h, --help            Print this command's help text and exit.
"""


@events.register(events.Event.CLI)
def register_command(argparser):
    cmd_parser = argparser.command("watch", helptext, cmd_callback)
    cmd_parser.flag("clear c")
    cmd_parser.option("theme t")
    cmd_parser.option("port p", type=int, default=8080)


# Callback for the watch command. Python doesn't have a builtin file system
# watcher so we hack together one of our own.
def cmd_callback(cmd_name, cmd_parser):
    home = site.home()
    if not home:
        sys.exit("Error: cannot locate the site's home directory.")

    # We want to reinvoke the currently active Ivy package when we call the
    # build command. This package may have been invoked in one of three ways:
    # 1. Directly: `python /path/to/ivy/directory`.
    # 2. As an installed package on the import path: `python -m ivy`.
    # 3. Via an entry script or Windows executable.
    if os.path.isdir(sys.argv[0]):
        base = ['python3', sys.argv[0]]
    elif sys.argv[0].endswith('__main__.py'):
        base = ['python3', sys.argv[0]]
    else:
        base = [sys.argv[0]]

    # Append the 'build' command, a 'watching' flag, and any user arguments.
    args = base + ['build', 'watching'] + cmd_parser.args

    # Add direct support for the 'build' command's options and flags.
    if cmd_parser.found('theme'):
        args += ['--theme', cmd_parser.value('theme')]
    if cmd_parser.found('clear'):
        args += ['--clear']

    # Print a header showing the site location.
    utils.termline()
    print("Site: %s" % home)
    print("Stop: Ctrl-C")
    utils.termline()

    # Build the site with the 'firstwatch' flag.
    subprocess.call(args + ['firstwatch'])
    utils.termline()

    # Create a hash digest of the site directory.
    oldhash = hashsite(home)

    # Run the webserver in a child process. It should run silently in the
    # background and automatically shut down when the watch process exits.
    subprocess.Popen(
        base + ['serve', '--port', str(cmd_parser.value('port'))],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Loop until the user hits Ctrl-C.
    try:
        while True:
            newhash = hashsite(home)
            if newhash != oldhash:
                subprocess.call(args)
                newhash = hashsite(home)
            oldhash = newhash
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass

    # Build the site with the 'lastwatch' flag.
    print()
    utils.termline()
    subprocess.call(args + ['lastwatch'])
    utils.termline()


# Return a hash digest of the site directory.
def hashsite(sitepath):
    hasher = hashlib.sha256()

    def hashdir(dirpath, is_home):
        for entry in os.scandir(dirpath):
            if entry.name.startswith('.') or entry.name.endswith('~'):
                continue
            if entry.is_file():
                mtime = os.path.getmtime(entry.path)
                hasher.update(str(mtime).encode())
                hasher.update(entry.name.encode())
            if entry.is_dir():
                hashdir(entry.path, False)

    try:
        hashdir(sitepath, True)
    except FileNotFoundError:
        pass

    return hasher.digest()
