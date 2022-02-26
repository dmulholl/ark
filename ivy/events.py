# ------------------------------------------------------------------------------
# This module implements the event API for extensions.
# ------------------------------------------------------------------------------

from enum import Enum, unique


# Dictionary mapping hook names to lists of callback functions indexed by order.
_callbacks = {}


# Enumeration of available events. String names are supported for backward
# compatibility.
@unique
class Event(Enum):
    """All events that Ivy understands are listed here."""
    CLI = "cli"
    DEPLOY = "deploy"
    EXIT = "exit"
    EXIT_BUILD = "exit_build"
    INIT = "init"
    INIT_BUILD = "init_build"
    MAIN = "main"
    MAIN_BUILD = "main_build"
    RENDER_PAGE = "render_page"


# Name-to-value lookup table for Event to support backward compatibility.
EVENT_NAMES = {member.value: member for member in Event}


# Decorator function for registering event callbacks, i.e. handler functions
# which will be called when the corresponding event hook is fired.
#
# Event callbacks accept zero or more arguments depending on the specific
# hook. They may modify their arguments in place but have no return value.
#
# The @register decorator accepts an optional order parameter with a default
# integer value of 0. Callbacks with lower order are called first.
#
# The hook parameter must be an Event or the name of an Event; the latter
# is translated into the former.
def register(hook, order=0):
    hook = _hook_enum(hook)

    def register_callback(callback):
        _callbacks.setdefault(hook, {}).setdefault(order, []).append(callback)
        return callback

    return register_callback


# Register an event callback directly without using a decorator.
def register_callback(hook, callback, order=0):
    hook = _hook_enum(hook)
    _callbacks.setdefault(hook, {}).setdefault(order, []).append(callback)


# Fires an event hook.
def fire(hook, *args):
    hook = _hook_enum(hook)
    for order in sorted(_callbacks.get(hook, {})):
        for func in _callbacks[hook][order]:
            func(*args)


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


# Ensure that hook identifier is an Event.
def _hook_enum(hook):
    if isinstance(hook, Event):
        return hook
    assert isinstance(hook, str), f"Hook name is not Event or string {hook}/{type(hook)}"
    assert hook in EVENT_NAMES, f"Unknown event hook name {hook}"
    return EVENT_NAMES[hook]
