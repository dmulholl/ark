# ------------------------------------------------------------------------------
# This module makes the `ivy` package directly executable. To run an `ivy` 
# package located on Python's import search path use:
#
#   $ python -m ivy
#
# To run an arbitrary `ivy` package use:
#
#   $ python /path/to/ivy/package
# ------------------------------------------------------------------------------

import os
import sys

# We need to manually add the package's parent directory to the module search 
# path before we can `import ivy`.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import ivy
sys.path.pop(0)

ivy.main()
