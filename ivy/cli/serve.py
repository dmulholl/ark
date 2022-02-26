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
Usage: ivy serve

  Serve the site's output directory using Python's builtin web server. The
  default web browser is automatically launched to view the site.

  Host IP defaults to localhost (127.0.0.1). Specify an IP address to serve
  only on that address or 0.0.0.0 to serve on all available IPs.

  Port number defaults to 8080. Setting the port number to 0 will randomly
  select an available port above 1024. Note that port numbers below 1024
  require root authorization.

Options:
  -d, --directory <path>    Specify a custom directory to serve.
  -h, --host <addr>         Host IP address. Defaults to localhost.
  -p, --port <int>          Port number. Defaults to 8080.

Flags:
      --help                Print this command's help text and exit.
"""


@events.register(events.Event.CLI)
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
    else:
        if not site.home():
            sys.exit("Error: cannot locate the site's home directory.")
        if not os.path.exists(site.out()):
            sys.exit("Error: cannot locate the site's output directory.")
        dirpath = site.out()

    os.chdir(dirpath)

    req_host = cmd_parser.value('host')
    req_port = cmd_parser.value('port')

    server_class = http.server.ThreadingHTTPServer
    handler_class = http.server.SimpleHTTPRequestHandler

    try:
        server = server_class((req_host, req_port), handler_class)
    except PermissionError:
        sys.exit("Error: use 'sudo' to run on a port below 1024.")
    except OSError:
        sys.exit("Error: port already in use. Choose a different port.")

    host, port = server.socket.getsockname()

    url = f"http://{req_host}:{port}"
    webbrowser.open(url)

    utils.termline()
    print("Root: %s" % dirpath)
    print("Host: %s"  % host)
    print("Port: %s" % port)
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
