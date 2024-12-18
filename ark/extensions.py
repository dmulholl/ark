# ------------------------------------------------------------------------------
# This module loads extensions, i.e. Python modules and packages which use Ark's
# plugin architecture to extend its functionality.
# ------------------------------------------------------------------------------

import os
import sys
import importlib
from . import site


# Load the named Python module from the specified directory.
def load_module(dirpath: str, name: str):
    sys.path.insert(0, dirpath)

    try:
        importlib.import_module(name)
    except Exception as e:
        raise Exception(f"Failed to load extension {name}: {e}") from e

    sys.path.pop(0)

# Load a directory of Python modules.
def load_directory(dirpath: str):
    for name in os.listdir(dirpath):
        if name.startswith('.'):
            continue
        path = os.path.join(dirpath, name)
        if os.path.isfile(path):
            base, ext = os.path.splitext(name)
            if ext == '.py':
                load_module(dirpath, base)
        elif os.path.isdir(path):
            load_module(dirpath, name)


# Load the default set of bundled extensions.
def load_bundled_extensions():
    load_directory(os.path.join(os.path.dirname(__file__), 'extensions'))


# Load extensions from the site directory.
def load_site_extensions():
    if os.path.isdir(site.ext()):
        load_directory(site.ext())


# Load installed extensions listed in the site's configuration file.
def load_installed_extensions():
    for name in site.config.get('extensions', []):
        importlib.import_module(name)


# Load extensions bundled with the active theme.
def load_theme_extensions():
    if site.theme() and os.path.isdir(site.theme('extensions')):
        load_directory(site.theme('extensions'))
