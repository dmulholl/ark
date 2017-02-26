# --------------------------------------------------------------------------
# Event and filter hooks.
# --------------------------------------------------------------------------

# Maps hook names to lists of callback functions indexed by order.
callbacks = {}


# Decorator function for registering event and filter callbacks, i.e.
# handler functions which will be called when the corresponding event or
# filter hook is fired.
#
# Event callbacks accept zero or more arguments depending on the specific
# hook. They may modify their arguments in place but have no return value.
#
# Filter callbacks accept at least one argument - the value to be filtered.
# They may accept additional arguments depending on the specific hook. Filter
# callbacks modify and return the value of their first argument.
#
# The @register decorator accepts an optional order parameter with a default
# value of 0. Callbacks with lower order fire before callbacks with
# higher order.
def register(hook, order=0):

    def register_callback(func):
        callbacks.setdefault(hook, {}).setdefault(order, []).append(func)
        return func

    return register_callback


# Fires an event hook.
def event(hook, *args):
    for order in sorted(callbacks.get(hook, {})):
        for func in callbacks[hook][order]:
            func(*args)


# Fires a filter hook.
def filter(hook, value, *args):
    for order in sorted(callbacks.get(hook, {})):
        for func in callbacks[hook][order]:
            value = func(value, *args)
    return value
