##
## Add support for Ibis template files with a `.ibis` extension.
##

import ivy

try:
    import ibis
except ImportError:
    ibis = None

if ibis:
    @ivy.events.register(ivy.events.Event.INIT)
    def initalize_template_loader():
        ibis.loader = ibis.loaders.FileLoader(ivy.site.theme('templates'))

    @ivy.templates.register('ibis')
    def render_page(page_data, template_filename):
        template = ibis.loader(template_filename)
        return template.render(page_data)
