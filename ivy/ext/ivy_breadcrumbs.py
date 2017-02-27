# --------------------------------------------------------------------------
# This extension generates a breadcrumb trail of links for each ancestor
# in a node's path.
# --------------------------------------------------------------------------

import ivy


@ivy.hooks.register('init_tree')
def generate_breadcrumb_trail(tree):
    tree.walk(callback)


def callback(node):

    # Assemble separate trails of names and links.
    names, links, current = [], [], node

    # Stop when 'current' is the root node.
    while current.parent is not None:
        name = current.get('title') or current.stem
        link = '<a href="%s">%s</a>' % (current['url'], name)
        names.append(name)
        links.append(link)
        current = current.parent

    names.reverse()
    links.reverse()

    node['crumbs'] = {'names': names, 'links': links}
