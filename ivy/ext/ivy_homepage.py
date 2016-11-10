# --------------------------------------------------------------------------
# This extension adds support for a customizable homepage index.
# --------------------------------------------------------------------------

from ivy import hooks, site


# Register a callback on the 'render_page' event hook..
@hooks.register('render_page')
def custom_homepage_callback(page):

    # If the page isn't the homepage, bail now.
    if page['node']['url'] != '@root/':
        return

    # Add a page flag for styling, etc.
    page['flags']['is_homepage'] = True

    # Default settings. Can be overridden via an 'index' attribute on the
    # homepage node.
    settings = {
        'path': '',
        'number': 10,
        'order_by': 'date',
        'reverse': True,
    }
    settings.update(page['node'].get('index', {}))

    # Node path of the form '/path/to/index/node'.
    path = settings['path']
    if not path:
        return

    node = nodes.node(*path.strip('/').split('/'))
    if not node:
        return

    order_attr = settings['order_by']
    nodes = [node for node in node.leaves() if order_attr in node]
    nodes.sort(key=lambda node: node[order_attr], reverse=self.reverse)

    number = settings['number'] or len(nodes)
    page['index'] = nodes[:number]
