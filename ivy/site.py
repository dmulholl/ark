# ------------------------------------------------------------------------------
# This module loads, processes, and caches the site's configuration data.
# ------------------------------------------------------------------------------

import os
import sys
import time
import pathlib

from . import renderers
from . import utils

from os.path import isdir, isfile, join
from typing import Dict


# This dictionary contains the content of the site's `config.py` file. It can
# be accessed in template files via the `site` variable.
config = {}


# Storage for temporary data generated during the build process.
cache = {}


# Initialize the site model.
def init():

    # Record the start time.
    cache['start_time'] = time.time()

    # Initialize a count of the number of pages rendered.
    cache['pages_rendered'] = 0

    # Initialize a count of the number of pages written to disk.
    cache['pages_written'] = 0

    # Default site configuration settings.
    config['root'] = ''
    config['theme'] = 'graphite'
    config['extension'] = '.html'

    # The Unix timestamp is useful as a cache-busting parameter.
    config['timestamp'] = int(time.time())

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


# Attempts to determine the path to the site's home directory. We use the
# presence of a 'config.py' file (or, deprecated, a '.ivy' file) to identify the
# home directory. We first test the current working directory, then its ancestor
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


# Returns the path to the site's home directory or an empty string if the
# home directory cannot be located. Appends arguments.
def home(*append: str) -> str:
    path = cache.get('home') or cache.setdefault('home', _find_home())
    return join(path, *append)


# Caches custom directory paths. Allows standard directory names (`src`, `out`,
# etc.) to be overridden in the config.py file.
def _dirpath(dirname: str, config_key: str) -> str:
    if cached := cache.get(config_key):
        return cached
    elif custom := config.get(config_key):
        return cache.setdefault(config_key, join(home(), custom))
    else:
        return cache.setdefault(config_key, home(dirname))


# Returns the path to the source directory. Appends arguments.
def src(*append: str) -> str:
    path = _dirpath('src', 'src_dir')
    return join(path, *append)


# Returns the path to the output directory. Appends arguments.
def out(*append: str) -> str:
    path = _dirpath('out', 'out_dir')
    return join(path, *append)


# Returns the path to the theme-library directory. Appends arguments.
def lib(*append: str) -> str:
    path = _dirpath('lib', 'lib_dir')
    return join(path, *append)


# Returns the path to the extensions directory. Appends arguments.
def ext(*append: str) -> str:
    path = _dirpath('ext', 'ext_dir')
    return join(path, *append)


# Returns the path to the includes directory. Appends arguments.
def inc(*append: str) -> str:
    path = _dirpath('inc', 'inc_dir')
    return join(path, *append)


# Returns the path to the resources directory. Appends arguments.
def res(*append: str) -> str:
    path = _dirpath('res', 'res_dir')
    return join(path, *append)


# Attempts to determine the path to the theme directory corresponding to
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
        return os.path.abspath(name)

    # A bundled theme directory in the application folder?
    bundled_theme = join(os.path.dirname(__file__), 'ini', 'lib', name)
    if isdir(bundled_theme):
        return bundled_theme

    return ''


# Returns the path to the theme directory or an empty string if the theme
# directory cannot be located. Appends arguments.
def theme(*append: str) -> str:
    if 'themepath' not in cache:
        cache['themepath'] = _find_theme(config['theme'])
    return join(cache['themepath'], *append)


# Returns the application runtime in seconds.
def runtime() -> float:
    return time.time() - cache['start_time']


# Increments the count of pages rendered by n and returns the new value.
def pages_rendered(n: int = 0) -> int:
    cache['pages_rendered'] += n
    return cache['pages_rendered']


# Increments the count of pages written by n and returns the new value.
def pages_written(n: int = 0) -> int:
    cache['pages_written'] += n
    return cache['pages_written']


# Returns a cached dictionary of rendered files from the `inc` directory.
# The dictionary's keys are the original filenames converted to lowercase
# with spaces and hyphens replaced by underscores.
def includes() -> Dict[str, str]:
    if not 'includes' in cache:
        cache['includes'] = {}
        if isdir(inc()):
            for path in pathlib.Path(inc()).iterdir():
                text, _ = utils.loadfile(path)
                ext = path.suffix.strip('.')
                key = path.stem.lower().replace(' ', '_').replace('-', '_')
                cache['includes'][key] = renderers.render(text, ext, str(path))
    return cache['includes']


# Deprecated aliases.
rendered = pages_rendered
written = pages_written
