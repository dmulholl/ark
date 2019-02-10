---
title: Themes
---

A theme is a collection of templates, styles, and scripts that together provide the look and feel for a site. Themes should be placed in the site's `lib` folder, and the name of the active theme directory specified in the site's configuration file.

::: python

    theme = "graphite"

Ivy ships with a small collection of bundled themes including `graphite`, a simple documentation theme, and `debug`, a diagnostic theme useful when designing themes or debugging sites.

Note that you can override the currently active theme with the `build` command's `--theme` flag:

    $ ivy build --theme debug

Ivy searches for a named theme first in the site's theme library, then (if it exists) in the global theme library specified by the `$IVY_THEMES` environment variable. Finally it searches among the default themes bundled with Ivy itself.



### Structure

Ivy looks for three subdirectories within the theme directory: `resources`, `extensions`, and `templates`.

* The content of the `resources` directory is copied to the output directory when the site is built.

* Themes can bundle extensions for Ivy by placing Python modules or packages in the `extensions` directory.

* The `templates` directory is where Ivy looks for the theme's template files.

Ivy has builtin support for templates written in [Jinja][] (using a `.jinja` extension) and [Ibis][] (using a `.ibis` extension). Support for other template languages can be added via plugins.

[Jinja]: http://jinja.pocoo.org
[Ibis]: https://github.com/dmulholland/ibis



### Templates

When Ivy generates a HTML page it searches for the appropriate template file to use in reverse order of specificity.

For example, the node file:

    src/foo/bar/baz.md

corresponds to the node:

    <Node /foo/bar/baz>

Ivy will search for a template file for this node in the following order:

    1. node-foo-bar-baz
    2. node-foo-bar
    3. node-foo
    4. node


A node can override this process by specifying a custom template file in its header:

    ---
    template: my-custom-template
    ---

Note that the file extension should be omitted from the template name.
