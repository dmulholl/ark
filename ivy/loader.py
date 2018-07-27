# ------------------------------------------------------------------------------
# This module is responsible for loading and preprocessing source files.
# ------------------------------------------------------------------------------

from . import hooks

from typing import Dict, Any, Union, Tuple
from pathlib import Path


# Load a source file. File metadata (e.g. yaml headers) can be extracted by
# preprocessor callbacks registered on the 'file_text' filter hook.
def load(path: Union[str, Path]) -> Tuple[str, Dict[str, Any]]:
    with open(str(path), encoding='utf-8') as file:
        text, meta = file.read(), {}
    text = hooks.filter('file_text', text, meta)
    for key, value in list(meta.items()):
        normalized_key = key.lower().replace(' ', '_').replace('-', '_')
        if normalized_key != key:
            del meta[key]
            meta[normalized_key] = value
    return text, meta
