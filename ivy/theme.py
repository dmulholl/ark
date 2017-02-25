# --------------------------------------------------------------------------
# This module loads extensions from the active theme directory.
# --------------------------------------------------------------------------

import os

from . import extensions
from . import site


# Load extension modules and packages bundled with the active theme.
def load():
    if site.theme() and os.path.isdir(site.theme('extensions')):
        extensions.load_directory(site.theme('extensions'))
