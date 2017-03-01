# --------------------------------------------------------------------------
# Loads, processes, and stores the site's configuration data.
# --------------------------------------------------------------------------

import os
import time
import sys

from os.path import isdir, isfile, join


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

    # Load the site's configuration file.
    load_site_config()


# Load and normalize the site's configuration data.
def load_site_config():

    # Default settings.
    config['root'] = ''
    config['theme'] = 'debug'
    config['extension'] = '.html'

    # Load the site configuration file.
    if home() and isfile(home('site.py')):
        with open(home('site.py'), encoding='utf-8') as file:
            exec(file.read(), config)

    # Delete the __builtins__ attribute as it pollutes variable dumps.
    if '__builtins__' in config:
        del config['__builtins__']

    # If 'root' isn't an empty string, make sure it ends in a slash.
    if config['root'] and not config['root'].endswith('/'):
        config['root'] += '/'


# Attempt to determine the path to the site's home directory. We check for
# the presence of either a 'site.py' file or both 'src' and 'out' directories.
# Returns an empty string if the home directory cannot be located.
def find_home():
    path = os.getcwd()
    while isdir(path):
        if isfile(join(path, 'site.py')):
            return os.path.abspath(path)
        elif isdir(join(path, 'src')) and isdir(join(path, 'out')):
            return os.path.abspath(path)
        path = join(path, '..')
    return ''


# Return the path to the site's home directory or an empty string if the
# home directory cannot be located. Append arguments.
def home(*append):
    path = cache.get('home') or cache.setdefault('home', find_home())
    return join(path, *append)


# Return the path to the source directory. Append arguments.
def src(*append):
    path = cache.get('src') or cache.setdefault('src', home('src'))
    return join(path, *append)


# Return the path to the output directory. Append arguments.
def out(*append):
    path = cache.get('out') or cache.setdefault('out', home('out'))
    return join(path, *append)


# Return the path to the theme-library directory. Append arguments.
def lib(*append):
    path = cache.get('lib') or cache.setdefault('lib', home('lib'))
    return join(path, *append)


# Return the path to the extensions directory. Append arguments.
def ext(*append):
    path = cache.get('ext') or cache.setdefault('ext', home('ext'))
    return join(path, *append)


# Return the path to the includes directory. Append arguments.
def inc(*append):
    path = cache.get('inc') or cache.setdefault('inc', home('inc'))
    return join(path, *append)


# Return the path to the resources directory. Append arguments.
def res(*append):
    path = cache.get('res') or cache.setdefault('res', home('res'))
    return join(path, *append)


# Attempt to determine the path to the theme directory corresponding to
# the specified theme name. Returns an empty string if the theme directory
# cannot be located.
def find_theme(name):

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


# Return the path to the theme directory. Append arguments.
def theme(*append):
    if 'themepath' not in cache:
        cache['themepath'] = find_theme(config['theme'])
    return join(cache['themepath'], *append)


# Return the application runtime in seconds.
def runtime():
    return time.time() - cache['start']


# Increment the count of pages rendered by n and return the new value.
def rendered(n=0):
    cache['rendered'] += n
    return cache['rendered']


# Increment the count of pages written by n and return the new value.
def written(n=0):
    cache['written'] += n
    return cache['written']
