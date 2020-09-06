# ------------------------------------------------------------------------------
# This module contains the logic for the 'serve' command.
# ------------------------------------------------------------------------------

import sys
import os
import http.server
import webbrowser

from .. import site
from .. import utils
from .. import events


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

""" % os.path.basename(sys.argv[0])


@events.register('cli')
def register_command(argparser):
    cmd_parser = argparser.command("serve", helptext, cmd_callback)
    cmd_parser.option("directory d")
    cmd_parser.option("browser b")
    cmd_parser.option("host h", default="localhost")
    cmd_parser.option("port p", type=int, default=8080)


def cmd_callback(cmd_name, cmd_parser):
    if cmd_parser.found('directory'):
        dirpath = os.path.abspath(cmd_parser.value('directory'))
        if not os.path.exists(dirpath):
            sys.exit(f"Error: directory '{dirpath}' does not exist.")
        os.chdir(dirpath)
    else:
        if not site.home():
            sys.exit("Error: cannot locate the site's home directory.")
        if not os.path.exists(site.out()):
            sys.exit("Error: cannot locate the site's output directory.")
        os.chdir(site.out())

    try:
        server = http.server.HTTPServer(
            (cmd_parser.value('host'), cmd_parser.value('port')),
            http.server.SimpleHTTPRequestHandler
        )
    except PermissionError:
        sys.exit("Error: use 'sudo' to run on a port below 1024.")
    except OSError:
        sys.exit("Error: port already in use. Choose a different port.")

    address = server.socket.getsockname()
    url = f"http://{cmd_parser.value('host')}:{address[1]}"
    if cmd_parser.found('browser'):
        try:
            browser = webbrowser.get(cmd_parser.value('browser'))
        except webbrowser.Error:
            sys.exit(f"Error: cannot locate browser '{cmd_parser.value('browser')}'.")
        browser.open(url)
    else:
        webbrowser.open(url)

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
