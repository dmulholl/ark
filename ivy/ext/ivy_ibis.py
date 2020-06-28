# ------------------------------------------------------------------------------
# This extension adds support for Ibis templates.
# ------------------------------------------------------------------------------

import ivy

try:
    import ibis
except ImportError:
    ibis = None


# The ibis package is an optional dependency.
if ibis:

    # Initialize the template loader.
    @ivy.events.register('init')
    def init():
        ibis.config.loader = ibis.loaders.FileLoader(
            ivy.site.theme('templates')
        )

    # Register our template engine callback for files with a .ibis extension.
    @ivy.templates.register('ibis')
    def callback(page, filename):
        template = ibis.config.loader(filename)
        return template.render(page)
