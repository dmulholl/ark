
# Ivy

Ivy is an experimental static website generator. It's powerful, flexible, and elegant.

Ivy is built in Python and runs on the command line:

    $ ivy --help

    Usage: ivy [FLAGS] [COMMAND]

      Ivy is a static website generator. It transforms a directory of text
      files into a self-contained website.

    Flags:
      --help              Print the application's help text and exit.
      --version           Print the application's version number and exit.

    Commands:
      build               Build the site.
      clear               Clear the output directory.
      init                Initialize a new site directory.
      serve               Run a web server on the site's output directory.
      watch               Monitor the site directory and rebuild on changes.

    Command Help:
      help <command>      Print the specified command's help text and exit.

Ivy is a successor to [Ark][]. Note that Ark is a mature, stable, and documented application; Ivy is unstable and undocumented. Breaking changes are guaranteed.

[ark]: https://github.com/dmulholland/ark



## Installation

Install directly from the Python Package Index using `pip`:

    $ pip install ivy

Ivy requires Python 3.5 or later.



## License

This work has been placed in the public domain.
