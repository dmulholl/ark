# ------------------------------------------------------------------------------
# This module implements the filter API for extensions.
# ------------------------------------------------------------------------------

from enum import Enum, unique


# Dictionary mapping hook names to lists of callback functions indexed by order.
_callbacks = {}


# Enumeration of available filters. String names are supposed for backward
# compatibility.
@unique
class Filter(Enum):
    """All filters that Ivy understands are listed here."""
    BUILD_NODE = "build_node"
    CLASS_LIST = "class_list"
    FILE_TEXT = "file_text"
    LOAD_NODE_DIR = "load_node_dir"
    LOAD_NODE_FILE = "load_node_file"
    NODE_HTML = "node_html"
    NODE_TEXT = "node_text"
    OUTPUT_FILEPATH = "output_filepath"
    PAGE_HTML = "page_html"
    SLUGIFY = "slugify"
    SLUG_LIST = "slug_list"
    TEMPLATE_LIST = "template_list"


# Name-to-value lookup table for Filter to support backward compatibility.
FILTER_NAMES = {member.value: member for member in Filter}


# Decorator function for registering filter callbacks, i.e. handler functions
# which will be called when the corresponding filter hook is fired.
#
# Filter callbacks accept at least one argument - the value to be filtered.
# They may accept additional arguments depending on the specific hook. Filter
# callbacks modify and return the value of their first argument.
#
# The @register decorator accepts an optional order parameter with a default
# integer value of 0. Callbacks with lower order fire first.
def register(hook, order=0):
    hook = _hook_enum(hook)

    def register_callback(callback):
        _callbacks.setdefault(hook, {}).setdefault(order, []).append(callback)
        return callback

    return register_callback


# Register a filter callback directly without using a decorator.
def register_callback(hook, callback, order=0):
    hook = _hook_enum(hook)
    _callbacks.setdefault(hook, {}).setdefault(order, []).append(callback)


# Fires a filter hook.
def apply(hook, value, *args):
    hook = _hook_enum(hook)
    for order in sorted(_callbacks.get(hook, {})):
        for func in _callbacks[hook][order]:
            value = func(value, *args)
    return value


# Clear all callbacks registered on a hook.
def clear(hook):
    hook = _hook_enum(hook)
    _callbacks[hook] = {}


# Deregister a callback from a hook.
def deregister(hook, callback, order=None):
    hook = _hook_enum(hook)
    if order is None:
        for order in _callbacks.get(hook, {}):
            if callback in _callbacks[hook][order]:
                _callbacks[hook][order].remove(callback)
    elif order in _callbacks[hook] and callback in _callbacks[hook][order]:
        _callbacks[hook][order].remove(callback)


# Ensure that hook identifier is an Filter.
def _hook_enum(hook):
    if isinstance(hook, Filter):
        return hook
    assert isinstance(hook, str), f"Hook name is not Filter or string {hook}/{type(hook)}"
    assert hook in FILTER_NAMES, f"Unknown filter hook name {hook}"
    return FILTER_NAMES[hook]
