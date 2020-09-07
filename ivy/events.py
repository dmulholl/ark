# ------------------------------------------------------------------------------
# This module implements the event API for extensions.
# ------------------------------------------------------------------------------

from typing import Callable, Any, Optional, Dict, List


# Dictionary mapping hook names to lists of callback functions indexed by order.
_callbacks: Dict[str, Dict[int, List[Callable]]] = {}


# Decorator function for registering event callbacks, i.e. handler functions
# which will be called when the corresponding event hook is fired.
#
# Event callbacks accept zero or more arguments depending on the specific
# hook. They may modify their arguments in place but have no return value.
#
# The @register decorator accepts an optional order parameter with a default
# integer value of 0. Callbacks with lower order are called first.
def register(hook: str, order: int = 0) -> Callable:

    def decorator(callback: Callable) -> Callable:
        _callbacks.setdefault(hook, {}).setdefault(order, []).append(callback)
        return callback

    return decorator


# Register an event callback directly without using a decorator.
def register_callback(hook: str, callback: Callable, order: int = 0):
    _callbacks.setdefault(hook, {}).setdefault(order, []).append(callback)


# Fires an event hook.
def fire(hook: str, *args: Any):
    for order in sorted(_callbacks.get(hook, {})):
        for func in _callbacks[hook][order]:
            func(*args)


# Clear all callbacks registered on a hook.
def clear(hook: str):
    _callbacks[hook] = {}


# Deregister a callback from a hook.
def deregister(hook: str, callback: Callable, order: Optional[int] = None):
    if order is None:
        for order in _callbacks.get(hook, {}):
            if callback in _callbacks[hook][order]:
                _callbacks[hook][order].remove(callback)
    elif order in _callbacks[hook] and callback in _callbacks[hook][order]:
        _callbacks[hook][order].remove(callback)
