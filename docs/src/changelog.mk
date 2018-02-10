---
title: Changelog
---


### 1.1.0.dev

* Refactor url rewriting as a separate module.

* Fix a Windows bug in the algorithm for finding the site's home directory.

* Remove deprecated pre-1.0 support for `site.py` site configuration files. These files should be renamed to `config.py`.



### 1.0.0

* First stable release. Future releases will adhere to [semantic versioning][semver] for changes which affect the theme or plugin API.

* This release adds support for Monk files with a `.mk` extension.

* The default port for the `serve` command has been changed from `0` to `8080`.

* The `watch` command now automatically launches the test server to view the site.

* We revert to the original algorithm for locating and rewriting `@root/` urls, i.e. only urls enclosed in quotes or angle brackets will be rewritten. (Quotes are preserved, angle brackets evaporate.)

[semver]: http://semver.org



### 0.9.0

* Ivy has been updated to support [Monk][] 1.0, the markup language previously named Syntex. Old `.stx` files will continue to be supported.

[monk]: http://mulholland.xyz/docs/monk/



### 0.8.0

* The argument-parsing library for the command line interface has been changed
  from [Clio][] to [Janus][].

* The default `graphite` theme now supports a meta description tag.

[clio]: http://mulholland.xyz/docs/clio/
[janus]: http://mulholland.xyz/docs/janus/



### 0.7.0

* The algorithm for locating and rewriting `@root/` urls has been changed.
  Previously only `@root/` urls enclosed in quotes or angle brackets were rewritten; now all `@root/` urls are rewritten unless escaped by a preceding backslash.



### 0.6.0

* The site configuration file has been renamed from `site.py` to `config.py`.
  Old `site.py` files will continue to be recognised.

  Some Python installations were confusing the `site.py` file with the standard library's `site` module, causing the interpreter to crash when Ivy was run from the site directory.
