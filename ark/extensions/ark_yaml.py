# Add support for YAML file headers.

import ark
import re

try:
    import yaml
except ImportError:
    yaml = None

if yaml:
    @ark.filters.register(ark.filters.Filter.FILE_TEXT)
    def parse_yaml_header(text, meta_dict):
        if text.startswith("---\n"):
            if match := re.match(r"^---\n(.*?\n)---\n", text, re.DOTALL):
                text = text[match.end(0):]
                data = yaml.safe_load(match.group(1))
                if isinstance(data, dict):
                    meta_dict.update(data)
        return text
