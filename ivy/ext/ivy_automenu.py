# ------------------------------------------------------------------------------
# This extension automatically generates a menu containing links to every node
# in the site. The menu can be accessed in templates via the 'automenu'
# attribute.
#
# If a node has a 'menu_title' attribute, its value will be used in the
# menu in place of the node's title.
#
# By default entries are ordered alphabetically by filename. Entry order can
# be customized by giving nodes an integer 'menu_order' attribute with
# lower orders coming first. The default order value is 0. (Note that the
# homepage is an exception and will always be the first entry in the menu.)
#
# If a node has a 'menu_exclude' attribute set to true, it will be excluded
# from the menu.
# ------------------------------------------------------------------------------

import ivy


# We generate the menu once and cache it for future use.
cache = None


# Register a callback to add the 'automenu' attribute to each page context.
@ivy.events.register('render_page')
def add_automenu(page):
    global cache
    if cache is None:
        cache = get_pagelist()
    page['automenu'] = cache


def get_pagelist():
    menu = ['<ul>\n']

    root = ivy.nodes.root()
    title = root.get('menu_title') or root.get('title') or 'Home'
    menu.append(f'<li><a href="@root/">{title}</a></li>\n')

    for child in sorted_children(root):
        if not child.empty and not child.get('menu_exclude'):
            add_node(child, menu)

    menu.append('</ul>')
    return ''.join(menu)


def add_node(node, menu):
    menu.append('<li>')

    title = node.get('menu_title') or node.get('title') or 'Untitled Node'
    menu.append(f'<a href="{node.url}">{title}</a>')

    if node.has_children:
        children = []
        for child in sorted_children(node):
            if not child.empty and not child.get('menu_exclude'):
                children.append(child)
        if children:
            menu.append('<ul>\n')
            for child in children:
                add_node(child, menu)
            menu.append('</ul>\n')

    menu.append('</li>\n')


def sorted_children(node):
    return sorted(node.children, key=lambda n: n.get('menu_order', 0))
