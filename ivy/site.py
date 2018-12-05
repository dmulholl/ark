# ------------------------------------------------------------------------------
# This module loads, processes, and caches the site's configuration data.
# ------------------------------------------------------------------------------

import os
import time
import sys

from os.path import isdir, isfile, join
from typing import Any


# Storage for the site's configuration data.
config = {}


# Storage for temporary data generated during the build process.
cache = {}


# Initialize the site model.
def init():

    # Record the start time.
    cache['start'] = time.time()

    # Initialize a count of the number of pages rendered.
    cache['rendered'] = 0

    # Initialize a count of the number of pages written to disk.
    cache['written'] = 0

    # Default site configuration settings.
    config['root'] = ''
    config['theme'] = 'graphite'
    config['extension'] = '.html'

    # Load the site configuration file.
    if home() and isfile(home('config.py')):
        with open(home('config.py'), encoding='utf-8') as file:
            exec(file.read(), config)

    # Delete the __builtins__ attribute as it pollutes variable dumps.
    if '__builtins__' in config:
        del config['__builtins__']

    # If 'root' isn't an empty string, make sure it ends in a slash.
    if config['root'] and not config['root'].endswith('/'):
        config['root'] += '/'


# Attempt to determine and return the path to the site's home directory. We use
# the presence of either a 'config.py' or '.ivy' file to identify the home
# directory. We first test the current working directory, then its ancestor
# directories in sequence until we reach the system root. If we make it all the
# way to the system root without finding a home directory then we must not be
# inside an initialized Ivy site; in this case we return an empty string.
def _find_home() -> str:
    path = os.path.abspath(os.getcwd())
    while True:
        if isfile(join(path, 'config.py')) or isfile(join(path, '.ivy')):
            return path
        path, tail = os.path.split(path)
        if tail == '':
            break
    return ''


# Return the path to the site's home directory or an empty string if the
# home directory cannot be located. Append arguments.
def home(*append: str) -> str:
    path = cache.get('home') or cache.setdefault('home', _find_home())
    return join(path, *append)


# Return the path to the source directory. Append arguments.
def src(*append: str) -> str:
    path = cache.get('src') or cache.setdefault('src', home('src'))
    return join(path, *append)


# Return the path to the output directory. Append arguments.
def out(*append: str) -> str:
    path = cache.get('out') or cache.setdefault('out', home('out'))
    return join(path, *append)


# Return the path to the theme-library directory. Append arguments.
def lib(*append: str) -> str:
    path = cache.get('lib') or cache.setdefault('lib', home('lib'))
    return join(path, *append)


# Return the path to the extensions directory. Append arguments.
def ext(*append: str) -> str:
    path = cache.get('ext') or cache.setdefault('ext', home('ext'))
    return join(path, *append)


# Return the path to the includes directory. Append arguments.
def inc(*append: str) -> str:
    path = cache.get('inc') or cache.setdefault('inc', home('inc'))
    return join(path, *append)


# Return the path to the resources directory. Append arguments.
def res(*append: str) -> str:
    path = cache.get('res') or cache.setdefault('res', home('res'))
    return join(path, *append)


# Attempt to determine the path to the theme directory corresponding to
# the specified theme name. Returns an empty string if the theme directory
# cannot be located.
def _find_theme(name: str) -> str:

    # A directory in the site's theme library?
    if isdir(lib(name)):
        return lib(name)

    # A directory in the global theme library?
    if os.getenv('IVY_THEMES'):
        if isdir(join(os.getenv('IVY_THEMES'), name)):
            return join(os.getenv('IVY_THEMES'), name)

    # A raw directory path?
    if isdir(name):
        return name

    # A bundled theme directory in the application folder?
    bundled = join(os.path.dirname(__file__), 'ini', 'lib', name)
    if isdir(bundled):
        return bundled

    return ''


# Return the path to the theme directory or an empty string if the theme
# directory cannot be located. Append arguments.
def theme(*append: str) -> str:
    if 'themepath' not in cache:
        cache['themepath'] = _find_theme(config['theme'])
    return join(cache['themepath'], *append)


# Return the application runtime in seconds.
def runtime() -> float:
    return time.time() - cache['start']


# Increment the count of pages rendered by n and return the new value.
def rendered(n: int = 0) -> int:
    cache['rendered'] += n
    return cache['rendered']


# Increment the count of pages written by n and return the new value.
def written(n: int = 0) -> int:
    cache['written'] += n
    return cache['written']
