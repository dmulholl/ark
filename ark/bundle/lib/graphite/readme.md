# Graphite

[1]: https://github.com/dmulholl/ark
[2]: https://fonts.google.com/specimen/Crimson+Text

A simple [Ark][1] theme designed for generating project documentation.

This theme will display the following attributes from the site's configuration
file in the site header:

* `title`
* `tagline`
* `version`


## Includes

This theme supports the following includes:

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


## Copy Buttons

All `<pre>` blocks get an automatically-generated 'copy' button for copying the
content to the clipboard.

To disable this button for an individual `<pre>` block, add a `no-copy` classs
to the `<pre>` tag, e.g. in HTML:

    <pre class="no-copy">
        No copy button.
    </pre>

Or in Syntext:

    ::: code .no-copy
        No copy button.

To disable the copy button completely, add the following setting to your site
configuration file:

    graphite = {
        "disable_copy_button": True,
    }


## License

This theme is distributed under the following license:

* All code is released under the Zero-Clause BSD license (0BSD).
* The bundled [Crimson Text][2] font is distributed under the SIL Open Font
  License.
