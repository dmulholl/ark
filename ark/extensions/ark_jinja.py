# Add support for Jinja template files with a `.jinja` extension.

import ark

try:
    import jinja2
except ImportError:
    jinja2 = None

jinja_environment = None

if jinja2:
    @ark.events.register(ark.events.Event.INIT)
    def initialize_jinja_environment():
        settings = {
            'loader': jinja2.FileSystemLoader(ark.site.theme('templates'))
        }
        settings.update(ark.site.config.get('jinja_settings', {}))
        global jinja_environment
        jinja_environment = jinja2.Environment(**settings)

    @ark.templates.register('jinja')
    def render_page(page_data, template_filename):
        template = jinja_environment.get_template(template_filename)
        return template.render(page_data)
