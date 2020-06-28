# ------------------------------------------------------------------------------
# This module handles template-engine callbacks.
# ------------------------------------------------------------------------------

from __future__ import annotations
from typing import Dict, List, Callable, Any, Optional
from pathlib import Path

import sys
import pathlib

from . import site
from . import utils
from . import pages


# Stores registered template-engine callbacks indexed by file extension.
_callbacks: Dict[str, Callable] = {}


# Caches a list of the theme's template files.
_cache: Optional[List[Path]] = None


# Decorator function for registering template-engine callbacks. A template-
# engine callback should accept a Page instance and a template filename and
# return a string of html.
#
# Callbacks are registered per file extension, e.g.
#
#   @ivy.templates.register('ibis')
#   def callback(page, filename):
#       ...
#       return html
#
def register(ext: str) -> Callable:

    def register_callback(callback: Callable) -> Callable:
        _callbacks[ext] = callback
        return callback

    return register_callback


# Render a Page instance into html.
def render(page: pages.Page) -> str:

    # Cache a list of the theme's template files for future calls.
    global _cache
    if _cache is None:
        root = site.theme('templates')
        _cache = [p for p in Path(root).iterdir() if p.is_file()]

    # Find the first template file matching the page's template list.
    for name in page['templates']:
        for path in _cache:
            if name == path.stem:
                ext = path.suffix.strip('.')
                if ext in _callbacks:
                    try:
                        return _callbacks[ext](page, path.name)
                    except Exception as err:
                        msg = "Template Error\n"
                        msg += f"  Template: {path.name}\n"
                        msg += f"  Page: {page['filepath']}\n"
                        msg += f"  {err.__class__.__name__}: {err}"
                        if (context := err.__context__):
                            msg += f"\n  Cause: {context.__class__.__name__}: {context}"
                        sys.exit(msg)
                else:
                    sys.exit(f"Error: unrecognised template extension '.{ext}'.")

    # Missing template file.
    sys.exit(f"Error: missing template file for page: '{page['filepath']}'.")
