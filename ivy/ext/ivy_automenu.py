# --------------------------------------------------------------------------
# This extension automatically generates a html menu containing links to
# every node in the site. The menu can be accessed in templates via an
# 'automenu' attribute.
# --------------------------------------------------------------------------

import ivy


# We generate the menu once and cache it for future use.
cache = None


# Register a callback to add the 'automenu' attribute to each page context.
@ivy.hooks.register('render_page')
def add_automenu(page):
    global cache
    if cache is None:
        cache = assemble_menu()
    page['automenu'] = cache


def assemble_menu():
    menu = ['<ul>\n']

    root = ivy.nodes.root()
    title = root.get('menu_title') or root.get('title') or 'Home'
    menu.append('<li><a href="@root/">%s</a></li>\n' % title)

    for child in root.childlist:
        add_node(child, menu)

    menu.append('</ul>')
    return ''.join(menu)


def add_node(node, menu):
    menu.append('<li>')

    title = node.get('menu_title') or node.get('title')or 'Untitled Node'
    menu.append('<a href="%s">%s</a>' % (node.url, title))

    if node.has_children:
        menu.append('<ul>\n')
        for child in node.childlist:
            add_node(child, menu)
        menu.append('</ul>\n')

    menu.append('</li>\n')
