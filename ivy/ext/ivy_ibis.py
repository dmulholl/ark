import ivy

try:
    import ibis
except ImportError:
    ibis = None

if ibis:

    # Initialize the template loader.
    @ivy.events.register('init')
    def init():
        ibis.loader = ibis.loaders.FileLoader(ivy.site.theme('templates'))

    # Register our template engine callback for files with a .ibis extension.
    @ivy.templates.register('ibis')
    def callback(page, filename):
        template = ibis.loader(filename)
        return template.render(page)
