# ------------------------------------------------------------------------------
# This module loads, processes, and caches the site's configuration data.
# ------------------------------------------------------------------------------

import os
import sys
import time
import pathlib

from . import renderers
from . import utils

from os.path import isdir, isfile, join, abspath


# This dictionary contains the content of the site's `config.py` file. It can
# be accessed in template files via the `site` variable.
config = {}


# Storage for temporary data generated during the build process.
cache = {}


# Initialize the site model.
def init():

    # Record the start time.
    cache["start_time"] = time.time()

    # Initialize a count of the number of pages rendered.
    cache["pages_rendered"] = 0

    # Initialize a count of the number of pages written to disk.
    cache["pages_written"] = 0

    # Default site configuration settings.
    config["theme"] = "graphite"
    config["root_url"] = ""
    config["file_extension"] = ".html"

    # The Unix timestamp is useful as a cache-busting parameter.
    config["timestamp"] = int(time.time())

    # Load the site configuration file.
    _, site_config_file = _find_site_directory()
    if site_config_file:
        with open(site_config_file, encoding="utf-8") as file:
            exec(file.read(), config)

    # Delete the __builtins__ attribute as it pollutes variable dumps.
    if "__builtins__" in config:
        del config["__builtins__"]

    # If "root_url" isn't an empty string, make sure it ends in a slash.
    if config["root_url"] and not config["root_url"].endswith("/"):
        config["root_url"] += "/"


# Returns a list of valid names for the site configuration file.
def _get_valid_config_file_names():
    if valid_names := os.environ.get("ARK_CONFIG_FILE"):
        return valid_names.split(":")
    else:
        return ("site.py", "config.py")


# Attempts to determine the path to the site's home directory and site
# configuration file. Tries the current working directory, then its ancestor
# directories in sequence until it reaches the system root. Returns the tuple
# (site_directory_path, site_config_file_path) on success, or a tuple
# of empty strings on failure.
def _find_site_directory() -> tuple[str, str]:
    valid_config_file_names = _get_valid_config_file_names()
    current_path = os.path.abspath(os.getcwd())
    while True:
        for name in valid_config_file_names:
            if isfile(join(current_path, name)):
                return current_path, join(current_path, name)
        current_path, tail = os.path.split(current_path)
        if tail == "":
            break
    return "", ""


# Returns the path to the site's home directory if it exists, otherwise an empty
# string. Appends arguments.
def home(*append: str) -> str:
    if home_path := cache.get("home_dir"):
        return join(home_path, *append)
    else:
        home_path, _ = _find_site_directory()
        cache["home_dir"] = home_path
        return join(home_path, *append)


# Returns the path to the source directory. Appends arguments.
def src(*append: str) -> str:
    if src_path := cache.get("src_dir"):
        return join(src_path, *append)
    else:
        src_name = config.get("src_dir") or os.environ.get("ARK_SRC_DIR") or "src"
        src_path = cache.setdefault("src_dir", join(home(), src_name))
        return join(src_path, *append)


# Returns the path to the output directory. Appends arguments.
def out(*append: str) -> str:
    if out_path := cache.get("out_dir"):
        return join(out_path, *append)
    else:
        out_name = config.get("out_dir") or os.environ.get("ARK_OUT_DIR") or "out"
        out_path = cache.setdefault("out_dir", join(home(), out_name))
        return join(out_path, *append)


# Returns the path to the theme library directory. Appends arguments.
def lib(*append: str) -> str:
    if lib_path := cache.get("lib_dir"):
        return join(lib_path, *append)
    else:
        lib_name = config.get("lib_dir") or os.environ.get("ARK_LIB_DIR") or "lib"
        lib_path = cache.setdefault("lib_dir", join(home(), lib_name))
        return join(lib_path, *append)


# Returns the path to the extensions directory. Appends arguments.
def ext(*append: str) -> str:
    if ext_path := cache.get("ext_dir"):
        return join(ext_path, *append)
    else:
        ext_name = config.get("ext_dir") or os.environ.get("ARK_EXT_DIR") or "ext"
        ext_path = cache.setdefault("ext_dir", join(home(), ext_name))
        return join(ext_path, *append)


# Returns the path to the includes directory. Appends arguments.
def inc(*append: str) -> str:
    if inc_path := cache.get("inc_dir"):
        return join(inc_path, *append)
    else:
        inc_name = config.get("inc_dir") or os.environ.get("ARK_INC_DIR") or "inc"
        inc_path = cache.setdefault("inc_dir", join(home(), inc_name))
        return join(inc_path, *append)


# Returns the path to the resources directory. Appends arguments.
def res(*append: str) -> str:
    if res_path := cache.get("res_dir"):
        return join(res_path, *append)
    else:
        res_name = config.get("res_dir") or os.environ.get("ARK_RES_DIR") or "res"
        res_path = cache.setdefault("res_dir", join(home(), res_name))
        return join(res_path, *append)


# Returns the path to the theme directory or an empty string if the theme
# directory cannot be located. Appends arguments.
def theme(*append: str) -> str:
    if theme_path := cache.get("theme_path"):
        return join(theme_path, *append)

    theme_name = config["theme"]

    if isdir(theme_name):
        theme_path = cache.setdefault("theme_path", abspath(theme_name))
        return join(theme_path, *append)

    if isdir(lib(theme_name)):
        theme_path = cache.setdefault("theme_path", abspath(lib(theme_name)))
        return join(theme_path, *append)

    if os.getenv("ARK_THEMES"):
        if isdir(join(os.getenv("ARK_THEMES"), theme_name)):
            theme_path = cache.setdefault("theme_path", abspath(join(os.getenv("ARK_THEMES", theme_name))))
            return join(theme_path, *append)

    bundled_theme = join(os.path.dirname(__file__), "bundle", "lib", theme_name)
    if isdir(bundled_theme):
        theme_path = cache.setdefault("theme_path", abspath(bundled_theme))
        return join(theme_path, *append)

    return ""


# Returns the application runtime in seconds.
def runtime() -> float:
    return time.time() - cache["start_time"]


# Increments the count of pages rendered by n and returns the new value.
def pages_rendered(n: int = 0) -> int:
    cache["pages_rendered"] += n
    return cache["pages_rendered"]


# Increments the count of pages written by n and returns the new value.
def pages_written(n: int = 0) -> int:
    cache["pages_written"] += n
    return cache["pages_written"]


# Returns a cached dictionary of rendered files from the `inc` directory.
# The dictionary's keys are the original filenames converted to lowercase
# with spaces and hyphens replaced by underscores.
def includes() -> dict[str, str]:
    if not "includes" in cache:
        cache["includes"] = {}
        if isdir(inc()):
            for path in pathlib.Path(inc()).iterdir():
                text, _ = utils.loadfile(path)
                ext = path.suffix.strip(".")
                key = path.stem.lower().replace(" ", "_").replace("-", "_")
                cache["includes"][key] = renderers.render(text, ext, str(path))
    return cache["includes"]


# Deprecated aliases.
rendered = pages_rendered
written = pages_written
