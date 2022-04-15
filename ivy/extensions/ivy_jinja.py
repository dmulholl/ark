##
## Add support for Jinja template files with a `.jinja` extension.
##

import ivy

try:
    import jinja2
except ImportError:
    jinja2 = None

jinja_environment = None

if jinja2:
    @ivy.events.register(ivy.events.Event.INIT)
    def initialize_jinja_environment():
        settings = {
            'loader': jinja2.FileSystemLoader(ivy.site.theme('templates'))
        }
        settings.update(ivy.site.config.get('jinja_settings', {}))
        global jinja_environment
        jinja_environment = jinja2.Environment(**settings)

    @ivy.templates.register('jinja')
    def render_page(page_data, template_filename):
        template = jinja_environment.get_template(template_filename)
        return template.render(page_data)
