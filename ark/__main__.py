# ------------------------------------------------------------------------------
# This module makes the `ark` package directly executable. To run an `ark`
# package located on Python's import search path use:
#
#   $ python -m ark
#
# To run an arbitrary `ark` package use:
#
#   $ python /path/to/ark/package
# ------------------------------------------------------------------------------

import os
import sys

# We need to manually add the package's parent directory to the module search
# path before we can `import ark`.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import ark
sys.path.pop(0)

ark.main()
