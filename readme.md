# Ark

Ark is a static website generator built in Python. It's small, elegant, and simple to use.

* [Documentation](http://www.dmulholl.com/docs/ark/master/)
* [Demo Site](http://www.dmulholl.com/demos/ark/)


## Installation

Install Ark from the Python Package Index using `pip`:

    pip install ark

Ark requires Python 3.10 or later.


## Usage

Ark is a command-line tool. To view its helptext, run `ark --help`:

    Usage: ark [command]

      Ark is a static website generator. It transforms a
      directory of text files into a self-contained website.

    Flags:
      -h, --help        Print the application's help text.
      -v, --version     Print the application's version.

    Commands:
      build             Build the site.
      clear             Clear the output directory.
      init              Initialize a new site directory.
      serve             Run the test server.
      tree              Print the site's node tree.
      watch             Monitor the site directory and
                        automatically rebuild on changes.

    Command Help:
      help <command>    Print the command's help text.


## License

Zero-Clause BSD (0BSD).
