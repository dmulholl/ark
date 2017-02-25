# --------------------------------------------------------------------------
# This module loads and renders files from the site's 'inc' directory.
# --------------------------------------------------------------------------

import os
import pathlib

from . import loader
from . import renderers
from . import site


# Dictionary of rendered files indexed by (normalized) filename.
cache = None


# Return a dictionary of rendered files from the 'inc' directory.
def load():

    # Load and cache the directory's contents.
    global cache
    if cache is None:
        cache = {}
        if os.path.isdir(site.inc()):
            for path in pathlib.Path(site.inc()).iterdir():
                stem, ext = path.stem, path.suffix.strip('.')
                if ext in renderers.callbacks:
                    text, _ = loader.load(path)
                    key = stem.lower().replace(' ', '_').replace('-', '_')
                    cache[key] = renderers.render(text, ext)

    return cache
