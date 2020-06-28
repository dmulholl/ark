# ------------------------------------------------------------------------------
# This extension adds support for YAML metadata headers in source files. YAML
# headers are identified by opening and closing '---' lines.
# ------------------------------------------------------------------------------

import ivy
import re

try:
    import yaml
except ImportError:
    pass
else:
    @ivy.filters.register('file_text')
    def parse_yaml(text, meta):
        if text.startswith("---\n"):
            match = re.match(r"^---\n(.*?\n)---\n+", text, re.DOTALL)
            if match:
                text = text[match.end(0):]
                data = yaml.safe_load(match.group(1))
                if isinstance(data, dict):
                    meta.update(data)
        return text
