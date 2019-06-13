# ------------------------------------------------------------------------------
# This extension adds support for YAML metadata headers in source files.
# YAML headers are identified by opening and closing '---' lines, e.g.
#
#   ---
#   title: My Important Document
#   author: John Doe
#   ---
#
# ------------------------------------------------------------------------------

import ivy
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None


# The yaml package is an optional dependency.
if yaml:

    # Register our preprocessor callback on the 'file_text' filter hook.
    @ivy.hooks.register('file_text')
    def parse_yaml(text, meta):
        if text.startswith("---\n"):
            match = re.match(r"^---\n(.*?\n)---\n+", text, re.DOTALL)
            if match:
                text = text[match.end(0):]
                data = yaml.safe_load(match.group(1))
                if isinstance(data, dict):
                    meta.update(data)
        return text
