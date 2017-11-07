---
title: Changelog
---


### 1.0.0

* First stable release. Future releases will adhere to [semantic versioning][semver].

* Adds support for Monk files with a `.mk` extension.

* The default port for the `serve` command has been changed from `0` to `8080`.

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

* The algorithm for locating and rewriting `\\@root/` urls has been changed.
  Previously only `\\@root/` urls enclosed in quotes or angle brackets were rewritten; now all `\\@root/` urls are rewritten unless escaped by a preceeding backslash.



### 0.6.0

* The site configuration file has been renamed from `site.py` to `config.py`.
  Old `site.py` files will continue to be recognised.

  Some Python installations were confusing the `site.py` file with the standard library's `site` module, causing the interpreter to crash when Ivy was run from the site directory.
