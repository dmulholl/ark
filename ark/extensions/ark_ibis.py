# Add support for Ibis template files with a `.ibis` extension.

import ark

try:
    import ibis
except ImportError:
    ibis = None

if ibis:
    @ark.events.register(ark.events.Event.INIT)
    def initalize_template_loader():
        ibis.loader = ibis.loaders.FileLoader(ark.site.theme('templates'))

    @ark.templates.register('ibis')
    def render_page(page_data, template_filename):
        template = ibis.loader(template_filename)
        return template.render(page_data)
