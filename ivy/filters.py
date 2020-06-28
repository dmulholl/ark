# ------------------------------------------------------------------------------
# This module implements the filter API for extensions.
# ------------------------------------------------------------------------------

from typing import Callable, Any, Optional, Dict, List


# Dictionary mapping hook names to lists of callback functions indexed by order.
_callbacks: Dict[str, Dict[int, List[Callable]]] = {}


# Decorator function for registering filter callbacks, i.e. handler functions
# which will be called when the corresponding filter hook is fired.
#
# Filter callbacks accept at least one argument - the value to be filtered.
# They may accept additional arguments depending on the specific hook. Filter
# callbacks modify and return the value of their first argument.
#
# The @register decorator accepts an optional order parameter with a default
# integer value of 0. Callbacks with lower order fire first.
def register(hook: str, order: int = 0) -> Callable:

    def register_callback(func: Callable) -> Callable:
        _callbacks.setdefault(hook, {}).setdefault(order, []).append(func)
        return func

    return register_callback


# Fires a filter hook.
def apply(hook: str, value: Any, *args: Any) -> Any:
    for order in sorted(_callbacks.get(hook, {})):
        for func in _callbacks[hook][order]:
            value = func(value, *args)
    return value


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
