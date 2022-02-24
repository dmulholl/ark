##
# This extension adds support for Ibis template files with a `.ibis` extension.
##

import ivy

try:
    import ibis
except ImportError:
    ibis = None

if ibis:

    # Initialize the template loader.
    @ivy.events.register(ivy.events.Event.INIT)
    def init():
        ibis.loader = ibis.loaders.FileLoader(ivy.site.theme('templates'))

    # Register our template engine callback for files with a .ibis extension.
    @ivy.templates.register('ibis')
    def callback(page_data, template_filename):
        template = ibis.loader(template_filename)
        return template.render(page_data)
