##
# This extension adds support for parsing YAML file headers.
##

import ivy
import re

try:
    import yaml
except ImportError:
    pass
else:
    @ivy.filters.register(ivy.filters.Filter.FILE_TEXT)
    def parse_yaml(text, meta_dict):
        if text.startswith("---\n"):
            if match := re.match(r"^---\n(.*?\n)---\n", text, re.DOTALL):
                text = text[match.end(0):]
                data = yaml.safe_load(match.group(1))
                if isinstance(data, dict):
                    meta_dict.update(data)
        return text
