---
title: Changelog
---


### 2.0.0-dev

* Add Python 3.6 type hints throughout the codebase.

* Update the minimum required Python version to 3.6.

* Remove the Vanilla theme from the default distribution.

* Refactor modules to clarify the distinction between public and private interfaces. Private methods and variables now have names beginning with an underscore.

* The default build process now skips empty nodes, i.e. nodes that correspond to a directory without an associated source file.

* Add Windows support for the `watch` command.

* Ivy now uses the presence of either a `config.py` file or a hidden `.ivy` file to identify a site's home directory.



### 1.3.0

* Remove deprecated support for source files in Syntex format.

* Minor improvements to Graphite theme styles.



### 1.2.0

* Add a sample plugin to the skeleton site's `ext` directory that registers an `\[% include %]` shortcode.



### 1.1.0

* Refactor url rewriting as a separate module.

* Fix a Windows bug in the algorithm for finding the site's home directory.

* Remove deprecated support for `site.py` site configuration files. These files should be renamed to `config.py`.



### 1.0.0

* First stable release. Future releases will adhere to [semantic versioning][semver] for changes which affect the theme or plugin API.

* This release adds support for Monk files with a `.mk` extension.

* The default port for the `serve` command has been changed from `0` to `8080`.

* The `watch` command now automatically launches the test server to view the site.

* We revert to the original algorithm for locating and rewriting `@root/` urls, i.e. only urls enclosed in quotes or angle brackets will be rewritten. (Quotes are preserved, angle brackets evaporate.)

[semver]: http://semver.org



### 0.9.0

* Ivy has been updated to support [Monk][] 1.0, the markup language previously named Syntex. Old `.stx` files will continue to be supported.

[monk]: https://darrenmulholland.com/docs/monk/



### 0.8.0

* The argument-parsing library for the command line interface has been changed
  from [Clio][] to [Janus][].

* The default `graphite` theme now supports a meta description tag.

[clio]: https://darrenmulholland.com/docs/clio/
[janus]: https://darrenmulholland.com/docs/janus/



### 0.7.0

* The algorithm for locating and rewriting `@root/` urls has been changed.
  Previously only `@root/` urls enclosed in quotes or angle brackets were rewritten; now all `@root/` urls are rewritten unless escaped by a preceding backslash.



### 0.6.0

* The site configuration file has been renamed from `site.py` to `config.py`.
  Old `site.py` files will continue to be recognised.

  Some Python installations were confusing the `site.py` file with the standard library's `site` module, causing the interpreter to crash when Ivy was run from the site directory.
