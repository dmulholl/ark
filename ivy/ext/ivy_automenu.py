##
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
##

import ivy


# We generate the menu once and cache it for future use.
cached_menu = None


# Register a callback to add an 'automenu' attribute to each page-data dictionary.
@ivy.events.register(ivy.events.Event.RENDER_PAGE)
def add_automenu(page_data):
    global cached_menu
    if cached_menu is None:
        cached_menu = make_menu()
    page_data['automenu'] = cached_menu


# This function's arguments are experimental and subject to change.
# - If `include_func` is set, it should accept a node and return true or false.
#   This determines whether a node is included in the menu or not.
# - If `sort_func` is set, it should accept a list of nodes and sort it in place.
#   This determines the ordering of nodes and subnodes in the memu.
def make_menu(include_func=None, sort_func=None):
    menu = ['<ul>\n']
    root = ivy.nodes.root()
    title = root.get('menu_title') or root.get('title') or 'Home'
    menu.append(f'<li><a href="@root/">{title}</a></li>\n')
    for node in sorted_children(root, include_func, sort_func):
        add_node_to_menu(node, menu, include_func, sort_func)
    menu.append('</ul>')
    return ''.join(menu)


def add_node_to_menu(node, menu, include_func, sort_func):
    title = node.get('menu_title') or node.get('title')
    menu.append('<li>')
    menu.append(f'<a href="{node.url}">{title}</a>')
    if children := sorted_children(node, include_func, sort_func):
        menu.append('<ul>\n')
        for child in children:
            add_node_to_menu(child, menu, include_func, sort_func)
        menu.append('</ul>\n')
    menu.append('</li>\n')


def sorted_children(node, include_func, sort_func):
    children = []
    for child in node.children:
        if include_func:
            if include_func(child):
                children.append(child)
        else:
            if child.get('menu_exclude'):
                continue
            if child.get('menu_title') is None and child.get('title') is None:
                continue
            if child.get('status', 'public').lower() in ('draft', 'private'):
                continue
            children.append(child)
    if sort_func:
        sort_func(children)
    else:
        children.sort(key=lambda node: node.stem)
        children.sort(key=lambda node: node.get('menu_order', 0))
    return children
