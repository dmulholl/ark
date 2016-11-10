# --------------------------------------------------------------------------
# This extension adds support for Ibis templates.
# --------------------------------------------------------------------------

import sys
from ivy import hooks, templates, site

try:
    import ibis
except ImportError:
    ibis = None


# The ibis package is an optional dependency.
if ibis:

    # Initialize our Ibis template loader on the 'init' event hook.
    @hooks.register('init')
    def init():
        ibis.config.loader = ibis.loaders.FileLoader(site.theme('templates'))

    # Register our template engine callback for files with a .ibis extension.
    @templates.register('ibis')
    def callback(page, filename):
        try:
            template = ibis.config.loader(filename)
            return template.render(page)
        except ibis.errors.TemplateError as err:
            msg =  "-----------------------\n"
            msg += "  Ibis Template Error  \n"
            msg += "-----------------------\n\n"
            msg += "  Template: %s\n" % filename
            msg += "  Page: %s\n\n" % page['filepath']
            msg += "  %s: %s" % (err.__class__.__name__, err)
            if err.__context__:
                cause = err.__context__
                msg += "\n\n  The following cause was reported:\n\n"
                msg += "  %s: %s" % (cause.__class__.__name__, cause)
            sys.exit(msg)
