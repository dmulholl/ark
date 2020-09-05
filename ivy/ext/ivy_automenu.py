# ------------------------------------------------------------------------------
# This extension automatically generates a menu containing links to every node
# in the site. The menu can be accessed in templates via an 'automenu' variable.
#
# If a node has a 'menu_title' attribute, its value will be used in the
# menu in place of the node's title.
#
# By default entries are ordered alphabetically by filename. Entry order can
# be customized by giving nodes an integer 'menu_order' attribute with
# lower orders coming first. The default order value is 0. (Note that the
# homepage is an exception and will always be the first entry in the menu.)
#
# If a node has a 'menu_exclude' attribute set to true or a 'status' attribute
# set to 'draft' or 'private' it will be excluded from the menu.
# ------------------------------------------------------------------------------

import ivy


# We generate the menu once and cache it for future use.
cache = None


# Register a callback to add an 'automenu' attribute to each Page instance.
@ivy.events.register('render_page')
def add_automenu(page):
    global cache
    if cache is None:
        cache = make_menu()
    page['automenu'] = cache


def make_menu():
    menu = ['<ul>\n']
    root = ivy.nodes.root()
    title = root.get('menu_title') or root.get('title') or 'Home'
    menu.append(f'<li><a href="@root/">{title}</a></li>\n')
    for entry in sorted_children(root):
        add_node_to_menu(entry[0], entry[1], menu)
    menu.append('</ul>')
    return ''.join(menu)


def add_node_to_menu(title, node, menu):
    menu.append('<li>')
    menu.append(f'<a href="{node.url}">{title}</a>')
    if entries := sorted_children(node):
        menu.append('<ul>\n')
        for entry in entries:
            add_node_to_menu(entry[0], entry[1], menu)
        menu.append('</ul>\n')
    menu.append('</li>\n')


def sorted_children(node):
    children = []
    for child in node.children:
        if child.get('menu_exclude'):
            continue
        if child.get('status', 'public').lower() in ('draft', 'private'):
            continue
        if (title := child.get('menu_title') or child.get('title')) is None:
            continue
        children.append((title, child))
    children.sort(key=lambda entry: entry[1].stem)
    children.sort(key=lambda entry: entry[1].get('menu_order', 0))
    return children

