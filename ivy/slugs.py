# --------------------------------------------------------------------------
# Slugification for path elements.
# --------------------------------------------------------------------------

import unicodedata
import re

from . import hooks


# Default slug-preparation function; returns a slugified version of the
# supplied string. This function is used to sanitize url components, etc.
def slugify(arg):
    out = unicodedata.normalize('NFKD', arg)
    out = out.encode('ascii', 'ignore').decode('ascii')
    out = out.lower()
    out = out.replace("'", '')
    out = re.sub(r'[^a-z0-9-]+', '-', out)
    out = re.sub(r'--+', '-', out)
    out = out.strip('-')
    return hooks.filter('slugify', out, arg)
