# ------------------------------------------------------------------------------
# This module contains the logic for the 'serve' command.
# ------------------------------------------------------------------------------

import sys
import os
import http.server
import webbrowser

from .. import site
from .. import utils
from .. import hooks


# Command help text.
helptext = """
Usage: %s serve

  Serve the site's output directory using Python's builtin web server. The
  default web browser is automatically launched to view the site.

  Host IP defaults to localhost (127.0.0.1). Specify an IP address to serve
  only on that address or 0.0.0.0 to serve on all available IPs.

  Port number defaults to 8080. Setting the port number to 0 will randomly
  select an available port above 1024. Note that port numbers below 1024
  require root authorization.

Options:
  -b, --browser <name>      Specify a browser to open by name.
  -d, --directory <path>    Specify a custom directory to serve.
  -h, --host <addr>         Host IP address. Defaults to localhost.
  -p, --port <int>          Port number. Defaults to 8080.

Flags:
      --help                Print this command's help text and exit.
      --no-browser          Do not launch the default web browser.

""" % os.path.basename(sys.argv[0])


# Register the command on the 'cli' event hook.
@hooks.register('cli')
def register_command(parser):
    cmd = parser.new_cmd("serve", helptext, callback)
    cmd.new_flag("no-browser")
    cmd.new_str("directory d")
    cmd.new_str("host h", fallback="localhost")
    cmd.new_int("port p", fallback=8080)
    cmd.new_str("browser b")


# Command callback.
def callback(parser):
    if parser['directory']:
        dirpath = os.path.abspath(parser['directory'])
        if not os.path.exists(dirpath):
            sys.exit("Error: directory '%s' does not exist." % dirpath)
        os.chdir(dirpath)
    else:
        if not site.home():
            sys.exit("Error: cannot locate the site's home directory.")
        if not os.path.exists(site.out()):
            sys.exit("Error: cannot locate the site's output directory.")
        os.chdir(site.out())

    try:
        server = http.server.HTTPServer(
            (parser['host'], parser['port']),
            http.server.SimpleHTTPRequestHandler
        )
    except PermissionError:
        sys.exit("Error: use 'sudo' to run on a port below 1024.")
    except OSError:
        sys.exit("Error: port already in use. Choose a different port.")

    address = server.socket.getsockname()
    if parser['browser']:
        try:
            browser = webbrowser.get(parser['browser'])
        except webbrowser.Error:
            sys.exit("Error: cannot locate browser '%s'." % parser['browser'])
        browser.open("http://%s:%s" % (parser['host'], address[1]))
    elif not parser['no-browser']:
        webbrowser.open("http://%s:%s" % (parser['host'], address[1]))

    utils.termline()
    print("Root: %s" % site.out())
    print("Host: %s"  % address[0])
    print("Port: %s" % address[1])
    print("Stop: Ctrl-C")
    utils.termline()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        utils.termline()
        print("Stopping server...")
        utils.termline()
        server.server_close()
