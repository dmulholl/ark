# ------------------------------------------------------------------------------
# This module implements the filter API for extensions.
# ------------------------------------------------------------------------------

# Dictionary mapping hook names to lists of callback functions indexed by order.
_callbacks = {}


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

    def register_callback(callback):
        _callbacks.setdefault(hook, {}).setdefault(order, []).append(callback)
        return callback

    return register_callback


# Register a filter callback directly without using a decorator.
def register_callback(hook, callback, order=0):
    _callbacks.setdefault(hook, {}).setdefault(order, []).append(callback)


# Fires a filter hook.
def apply(hook, value, *args):
    for order in sorted(_callbacks.get(hook, {})):
        for func in _callbacks[hook][order]:
            value = func(value, *args)
    return value


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
