# --------------------------------------------------------------------------
# This module loads theme extensions.
# --------------------------------------------------------------------------

import os

from . import extensions
from . import site


# Load extensions bundled with the active theme.
def load():
    if site.theme() and os.path.isdir(site.theme('extensions')):
        extensions.load_directory(site.theme('extensions'))
