# ------------------------------------------------------------------------------
# This module loads extensions, i.e. Python modules and packages which use
# Ivy's plugin architecture to extend its functionality.
# ------------------------------------------------------------------------------

import os
import sys
import importlib

from . import site


# Load the named Python module from the specified directory.
def load_module(directory: str, name: str):
    sys.path.insert(0, directory)
    importlib.import_module(name)
    sys.path.pop(0)


# Load a directory of Python modules.
def load_directory(directory: str):
    for name in os.listdir(directory):
        if name.startswith('.'):
            continue
        base = os.path.splitext(name)[0]
        load_module(directory, base)


# Load Ivy's default set of bundled extensions.
def load_bundled_extensions():
    load_directory(os.path.join(os.path.dirname(__file__), 'ext'))


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
