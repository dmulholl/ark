# ------------------------------------------------------------------------------
# This module is responsible for loading and preprocessing source files.
# ------------------------------------------------------------------------------

from . import hooks

from typing import Dict, Any, Union, Tuple
from pathlib import Path


# Load a source file. File metadata (e.g. yaml headers) can be extracted by
# preprocessor callbacks registered on the 'file_text' filter hook.
def load(path: Union[str, Path]) -> Tuple[str, Dict[str, Any]]:
    try:
        with open(str(path), encoding='utf-8') as file:
            text, meta = file.read(), {}
        text = hooks.filter('file_text', text, meta)
        for key, value in list(meta.items()):
            normalized_key = key.lower().replace(' ', '_').replace('-', '_')
            if normalized_key != key:
                del meta[key]
                meta[normalized_key] = value
        return text, meta
    except Exception as err:
        msg =  f"Error loading: {path}\n"
        msg += f"{err.__class__.__name__}: {err}\n"
        if err.__context__:
            msg += "The following cause was reported:\n"
            msg += "{err.__context__.__class__.__name__}: {err.__context__}"
        sys.exit(msg.strip())
