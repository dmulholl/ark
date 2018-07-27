# ------------------------------------------------------------------------------
# This module loads and renders source files from the site's 'inc' directory.
# ------------------------------------------------------------------------------

import os
import pathlib

from . import loader
from . import renderers
from . import site

from typing import Dict, Optional


# Dictionary of rendered files indexed by normalized filename.
_cache: Optional[Dict[str, str]] = None


# Return a dictionary of rendered files from the 'inc' directory.
def load() -> Dict[str, str]:
    global _cache
    if _cache is None:
        _cache = {}
        if os.path.isdir(site.inc()):
            for path in pathlib.Path(site.inc()).iterdir():
                stem, ext = path.stem, path.suffix.strip('.')
                if renderers.is_registered_ext(ext):
                    text, _ = loader.load(path)
                    key = stem.lower().replace(' ', '_').replace('-', '_')
                    _cache[key] = renderers.render(text, ext)
    return _cache
