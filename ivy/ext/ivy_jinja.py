##
# This extension adds support for Jinja template files with a `.jinja` extension.
##

import ivy

try:
    import jinja2
except ImportError:
    jinja2 = None


# Stores an initialized Jinja environment instance.
env = None


# The jinja2 package is an optional dependency.
if jinja2:

    # Initialize the Jinja environment on the 'init' event hook.
    # Check the site's config file for custom settings.
    @ivy.events.register(ivy.events.Event.INIT)
    def init():
        settings = {
            'loader': jinja2.FileSystemLoader(ivy.site.theme('templates'))
        }
        settings.update(ivy.site.config.get('jinja_settings', {}))
        global env
        env = jinja2.Environment(**settings)

    # Register our template engine callback for files with a .jinja extension.
    @ivy.templates.register('jinja')
    def callback(page_data, template_filename):
        template = env.get_template(template_filename)
        return template.render(page_data)
