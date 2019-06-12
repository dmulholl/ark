# ------------------------------------------------------------------------------
# This extension adds support for Ibis templates.
# ------------------------------------------------------------------------------

import sys
from ivy import hooks, templates, site

try:
    import ibis
except ImportError:
    ibis = None


# The ibis package is an optional dependency.
if ibis:

    # Initialize our template loader on the 'init' event hook.
    @hooks.register('init')
    def init():
        ibis.config.loader = ibis.loaders.FileLoader(site.theme('templates'))

    # Register our template engine callback for files with a .ibis extension.
    @templates.register('ibis')
    def callback(page, filename):
        template = ibis.config.loader(filename)
        return template.render(page)
