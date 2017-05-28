# --------------------------------------------------------------------------
# Logic for the 'watch' command.
# --------------------------------------------------------------------------

import sys
import os
import hashlib
import time
import subprocess
import hashlib
import shutil

from .. import site
from .. import utils


# Command help text.
helptext = """
Usage: %s watch [FLAGS] [ARGUMENTS]

  Monitor the site directory and automatically rebuild when file changes are
  detected.

Options:
  -i, --inc <path>      Override the default 'inc' directory.
  -l, --lib <path>      Override the default 'lib' directory.
  -o, --out <path>      Override the default 'out' directory.
  -r, --res <path>      Override the default 'res' directory.
  -s, --src <path>      Override the default 'src' directory.
  -t, --theme <name>    Override the default theme.

Flags:
  -c, --clear           Clear the output directory before each build.
      --help            Print this command's help text and exit.

""" % os.path.basename(sys.argv[0])


# Callback for the watch command. Python doesn't have a builtin file system
# watcher so we hack together one of our own.
def callback(parser):

    home = site.home()
    if not home:
        sys.exit("Error: cannot locate the site's home directory.")

    # Assemble a list of arguments for the subprocess call.
    args = []

    # We need to check if the `ivy` package has been executed:
    # 1. Directly, as `python3 /path/to/ivy/package`.
    # 2. As an installed package on the import path, `python3 -m ivy`.
    # 3. Via an entry script, `ivy`.
    if os.path.isdir(sys.argv[0]):
        args += ['python3', sys.argv[0]]
    elif os.path.isfile(sys.argv[0]) and sys.argv[0].endswith('__main__.py'):
        args += ['python3', sys.argv[0]]
    elif os.path.isfile(sys.argv[0]):
        args.append(sys.argv[0])

    # Append the 'build' command, a 'watching' flag, and any user arguments.
    args += ['build', 'watching'] + parser.get_args()

    # Add direct support for the 'build' command's options and flags.
    if parser['out']: args += ['--out', parser['out']]
    if parser['src']: args += ['--src', parser['src']]
    if parser['lib']: args += ['--lib', parser['lib']]
    if parser['inc']: args += ['--inc', parser['inc']]
    if parser['res']: args += ['--res', parser['res']]
    if parser['theme']: args += ['--theme', parser['theme']]
    if parser['clear']: args += ['--clear']

    # Determine terminal width.
    cols, _ = shutil.get_terminal_size()

    # Print a header showing the site location.
    print("─" * cols)
    print("Site: %s" % home)
    print("Stop: Ctrl-C")
    print("─" * cols)

    # Build the site with the 'firstwatch' flag.
    subprocess.call(args + ['firstwatch'])
    print("─" * cols)

    # Create a hash digest of the site directory.
    oldhash = hashsite(home)

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
    print("\n" + "─" * cols)
    subprocess.call(args + ['lastwatch'])
    print("─" * cols)


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
