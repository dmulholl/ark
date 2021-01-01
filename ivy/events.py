# ------------------------------------------------------------------------------
# This module implements the event API for extensions.
# ------------------------------------------------------------------------------

# Dictionary mapping hook names to lists of callback functions indexed by order.
_callbacks = {}


# Decorator function for registering event callbacks, i.e. handler functions
# which will be called when the corresponding event hook is fired.
#
# Event callbacks accept zero or more arguments depending on the specific
# hook. They may modify their arguments in place but have no return value.
#
# The @register decorator accepts an optional order parameter with a default
# integer value of 0. Callbacks with lower order are called first.
def register(hook, order=0):

    def register_callback(callback):
        _callbacks.setdefault(hook, {}).setdefault(order, []).append(callback)
        return callback

    return register_callback


# Register an event callback directly without using a decorator.
def register_callback(hook, callback, order=0):
    _callbacks.setdefault(hook, {}).setdefault(order, []).append(callback)


# Fires an event hook.
def fire(hook, *args):
    for order in sorted(_callbacks.get(hook, {})):
        for func in _callbacks[hook][order]:
            func(*args)


# Clear all callbacks registered on a hook.
def clear(hook):
    _callbacks[hook] = {}


# Deregister a callback from a hook.
def deregister(hook, callback, order=None):
    if order is None:
        for order in _callbacks.get(hook, {}):
            if callback in _callbacks[hook][order]:
                _callbacks[hook][order].remove(callback)
    elif order in _callbacks[hook] and callback in _callbacks[hook][order]:
        _callbacks[hook][order].remove(callback)
