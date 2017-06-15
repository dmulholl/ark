# --------------------------------------------------------------------------
# Logic for the 'serve' command.
# --------------------------------------------------------------------------

import sys
import os
import http.server
import webbrowser
import shutil

from .. import site


# Command help text.
helptext = """
Usage: %s serve [FLAGS] [OPTIONS]

  Serve the site's output directory using Python's builtin web server. The
  default web browser is automatically launched to view the site.

  Host IP defaults to localhost (127.0.0.1). Specify an IP address to serve
  only on that address or '0.0.0.0' to serve on all available IPs.

  Port number defaults to 0 which randomly selects an available port. Note
  that port numbers below 1024 require root authorization.

Options:
  -b, --browser <str>       Specify a browser to open by name.
  -d, --directory <path>    Specify a custom directory to serve.
  -h, --host <str>          Host IP address. Defaults to localhost.
  -p, --port <int>          Port number. Defaults to 0, i.e. random.

Flags:
      --help                Print this command's help text and exit.
      --no-browser          Do not launch the default web browser.

""" % os.path.basename(sys.argv[0])


# Command callback.
def callback(parser):

    if parser['directory']:
        if not os.path.exists(parser['directory']):
            sys.exit("Error: '%s' does not exist." % parser['directory'])
        os.chdir(parser['directory'])
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
        sys.exit("Error: address already in use. Choose a different port.")

    address = server.socket.getsockname()

    if parser['browser']:
        try:
            browser = webbrowser.get(parser['browser'])
        except webbrowser.Error:
            sys.exit("Error: cannot locate browser '%s'." % parser['browser'])
        browser.open("http://%s:%s" % (parser['host'], address[1]))
    elif not parser['no-browser']:
        webbrowser.open("http://%s:%s" % (parser['host'], address[1]))

    cols, _ = shutil.get_terminal_size()
    print("─" * cols)
    print("Root: %s" % site.out())
    print("Host: %s"  % address[0])
    print("Port: %s" % address[1])
    print("Stop: Ctrl-C")
    print("─" * cols)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n" + "─" * cols)
        print("Stopping server...")
        print("─" * cols)
        server.server_close()
