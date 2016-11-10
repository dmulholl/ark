# --------------------------------------------------------------------------
# This module makes the `ivy` package directly executable.
#
# To run an `ivy` package located on Python's import search path:
#
#   $ python -m ivy
#
# To run an arbitrary `ivy` package:
#
#   $ python /path/to/ivy/package
#
# This latter form can be used for running development versions of Ivy.
# --------------------------------------------------------------------------

import os
import sys


# Python doesn't automatically add the package's parent directory to the
# module search path so we need to do so manually before we can import `ivy`.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


import ivy
ivy.main()
