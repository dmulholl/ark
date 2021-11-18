# Graphite

[1]: https://github.com/dmulholl/ivy
[2]: https://fonts.google.com/specimen/Crimson+Text

A simple [Ivy][1] theme designed for generating project documentation.

This theme will display the following attributes from the site's `config.py` file in the site header:

* `title`
* `tagline`
* `version`

It supports the following includes:

* `menu`

    This file will be used to construct the theme's main menu. It should contain
    a list of links, optionally with nested sub-lists.

* `head`

    If a `head.html` file is present in the includes folder its content will be
    included at the end of each page's `<head>` section. This file can be used
    to add custom CSS or JavaScript to a site without directly editing the
    theme's template files.

* `foot`

    If a `foot.html` file is present in the includes folder its content will
    be included at the end of each page's `<body>` section. This file can be
    used to add custom JavaScript to a site without directly editing the
    theme's template files.

This theme is distributed under the following license:

* All code has been placed in the public domain.
* The bundled [Crimson Text][2] font is distributed under the SIL Open Font License.
