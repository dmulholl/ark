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
    @ivy.filters.register('file_text')
    def parse_yaml(raw_text, meta_dict):
        if raw_text.startswith("---\n"):
            if match := re.match(r"^---\n(.*?\n)---\n", raw_text, re.DOTALL):
                filtered_text = raw_text[match.end(0):]
                data = yaml.safe_load(match.group(1))
                if isinstance(data, dict):
                    meta_dict.update(data)
        return filtered_text
