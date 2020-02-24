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
from .. import hooks


# Command help text.
helptext = """
Usage: %s watch

  Monitor the site directory and automatically rebuild the site when file
  changes are detected.

  The test server is automatically launched to view the site.

Options:
  -i, --inc <path>      Override the default 'inc' directory.
  -l, --lib <path>      Override the default 'lib' directory.
  -o, --out <path>      Override the default 'out' directory.
  -p, --port <int>      Port number to serve on. Defaults to 8080.
  -r, --res <path>      Override the default 'res' directory.
  -s, --src <path>      Override the default 'src' directory.
  -t, --theme <name>    Override the default theme.

Flags:
  -c, --clear           Clear the output directory before each build.
  -h, --help            Print this command's help text and exit.
      --no-server       Do not launch the test server.

""" % os.path.basename(sys.argv[0])


# Register the command on the 'cli' event hook.
@hooks.register('cli')
def register_command(parser):
    cmd = parser.new_cmd("watch", helptext, callback)
    cmd.new_flag("clear c")
    cmd.new_flag("no-server")
    cmd.new_str("out o")
    cmd.new_str("src s")
    cmd.new_str("lib l")
    cmd.new_str("inc i")
    cmd.new_str("res r")
    cmd.new_str("theme t")
    cmd.new_int("port p", fallback=8080)


# Callback for the watch command. Python doesn't have a builtin file system
# watcher so we hack together one of our own.
def callback(parser):
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
    args = base + ['build', 'watching'] + parser.get_args()

    # Add direct support for the 'build' command's options and flags.
    if parser['out']: args += ['--out', parser['out']]
    if parser['src']: args += ['--src', parser['src']]
    if parser['lib']: args += ['--lib', parser['lib']]
    if parser['inc']: args += ['--inc', parser['inc']]
    if parser['res']: args += ['--res', parser['res']]
    if parser['theme']: args += ['--theme', parser['theme']]
    if parser['clear']: args += ['--clear']

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
    if not parser["no-server"]:
        subprocess.Popen(
            base + ['serve', '--port', str(parser['port'])],
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
            time.sleep(0.25)
    except KeyboardInterrupt:
        pass

    # Build the site with the 'lastwatch' flag.
    print()
    utils.termline()
    subprocess.call(args + ['lastwatch'])
    utils.termline()


# Return a hash digest of the site directory.
def hashsite(sitepath):
    hash = hashlib.sha256()

    def hashdir(dirpath, is_home):
        for entry in os.scandir(dirpath):
            if entry.is_file():
                if entry.name.endswith('~'):
                    continue
                mtime = os.path.getmtime(entry.path)
                hash.update(str(mtime).encode())
                hash.update(entry.name.encode())
            if entry.is_dir():
                if is_home and entry.name == 'out':
                    continue
                hashdir(entry.path, False)

    hashdir(sitepath, True)
    return hash.digest()
