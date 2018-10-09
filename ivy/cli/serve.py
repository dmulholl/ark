# ------------------------------------------------------------------------------
# This module contains the logic for the 'serve' command.
# ------------------------------------------------------------------------------

import sys
import os
import http.server
import webbrowser
import shutil
import ssl

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
  -c, --ssl-cert <path>     SSL certificate file. (Enables HTTPS.)
  -k, --ssl-key <path>      SSL key file if separate from certificate.

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
    cmd.new_str("ssl-cert c")
    cmd.new_str("ssl-key k")


# Command callback.
def callback(parser):

    if parser['ssl-cert']:
        certfile = os.path.abspath(parser['ssl-cert'])
        if not os.path.exists(certfile):
            sys.exit("Error: certificate '%s' does not exist." % certfile)
    else:
        certfile = None

    if parser['ssl-key']:
        keyfile = os.path.abspath(parser['ssl-key'])
        if not os.path.exists(keyfile):
            sys.exit("Error: key file '%s' does not exist." % keyfile)
    else:
        keyfile = None

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

    if certfile:
        server.socket = ssl.wrap_socket(
            server.socket,
            keyfile=keyfile,
            certfile=certfile,
            server_side=True
        )
        protocol = "https"
    else:
        protocol = "http"

    address = server.socket.getsockname()
    if parser['browser']:
        try:
            browser = webbrowser.get(parser['browser'])
        except webbrowser.Error:
            sys.exit("Error: cannot locate browser '%s'." % parser['browser'])
        browser.open("%s://%s:%s" % (protocol, parser['host'], address[1]))
    elif not parser['no-browser']:
        webbrowser.open("%s://%s:%s" % (protocol, parser['host'], address[1]))

    cols, _ = shutil.get_terminal_size()
    utils.safeprint("─" * cols)
    utils.safeprint("Root: %s" % site.out())
    utils.safeprint("Host: %s"  % address[0])
    utils.safeprint("Port: %s" % address[1])
    utils.safeprint("Stop: Ctrl-C")
    utils.safeprint("─" * cols)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        utils.safeprint("\n" + "─" * cols)
        utils.safeprint("Stopping server...")
        utils.safeprint("─" * cols)
        server.server_close()
