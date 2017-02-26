# --------------------------------------------------------------------------
# This module adds support for multi-page indexes.
# --------------------------------------------------------------------------

import math

from . import hooks, pages


# An Index instance represents a numbered collection of index pages.
class Index:

    # Every Index is initialized with an associated Node instance. This
    # node's location in the parse tree determines the output path for
    # the Index's individual Page instances.
    def __init__(self, node, nodes, per_page=None):

        # Filter and sort the node list.
        order_by = node.get('order_by', 'date')
        reverse = node.get('reverse', True)
        nodes = [node for node in nodes if order_by in node]
        nodes.sort(key=lambda node: node[order_by], reverse=reverse)

        # How many pages do we need?
        if per_page is None:
            per_page = node.get('per_index', 10)
        if per_page == 0:
            per_page = len(nodes) or 1
        total = math.ceil(float(len(nodes)) / per_page)

        # Create the required number of pages.
        self.pages = []
        for i in range(1, total + 1):
            page = pages.Page(node)
            self.pages.append(page)

            page['index'] = nodes[per_page * (i - 1) : per_page * i]
            page['flags']['is_index'] = True
            page['flags']['is_paged'] = (total > 1)

            page['paging']['page'] = i
            page['paging']['total'] = total
            page['paging']['first_url'] = node.paged_url(1, total)
            page['paging']['prev_url'] = node.paged_url(i - 1, total)
            page['paging']['next_url'] = node.paged_url(i + 1, total)
            page['paging']['last_url'] = node.paged_url(total, total)

    # Render each page in the index into html and write it to disk.
    def render(self):
        for page in self.pages:
            page.render()

    # Set a flag attribute on all the index's individual Page instances.
    def set_flag(self, key, value):
        for page in self.pages:
            page['flags'][key] = value


# Instantiating a LeafIndex constructs an index listing all leaf-nodes
# descending from the specified node.
class LeafIndex(Index):

    def __init__(self, node):
        super().__init__(node, node.leaves())
        self.set_flag('is_leaf_index', True)
