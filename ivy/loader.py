# --------------------------------------------------------------------------
# This module loads and preprocesses source files.
# --------------------------------------------------------------------------

from . import hooks


# Load a source file. File metadata (e.g. yaml headers) can be extracted by
# preprocessor callbacks registered on the 'file_text' filter hook.
def load(path):
    with open(str(path), encoding='utf-8') as file:
        text, meta = file.read(), {}
    text = hooks.filter('file_text', text, meta)
    return text, normalize(meta)


# Normalize a metadata dictionary's keys.
def normalize(meta):
    output = {}
    for key, value in meta.items():
        output[key.lower().replace(' ', '_').replace('-', '_')] = value
    return output
