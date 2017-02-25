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
    def __init__(self, node, nodes):
        self.node = node
        self.nodes = nodes
        self.order_by = node.get('order_by', 'date')
        self.per_page = node.get('per_index', 10)
        self.reverse = node.get('reverse', True)

    # Initialize the index by creating the required number of individual
    # Page instances.
    def init(self):

        # Discard any nodes that lack the requisite order_by attribute.
        nodes = [node for node in self.nodes if self.order_by in node]

        # Sort the nodes.
        nodes.sort(key=lambda n: n[self.order_by], reverse=self.reverse)

        # How many pages do we need?
        per_page = self.per_page or len(nodes) or 1
        total = math.ceil(float(len(nodes)) / per_page)

        # Create the required number of pages.
        self.pages = []
        for i in range(1, total + 1):
            page = pages.Page(self.node)
            self.pages.append(page)

            page['index'] = nodes[per_page * (i - 1) : per_page * i]
            page['flags']['is_index'] = True
            page['flags']['is_paged'] = (total > 1)

            page['paging']['page'] = i
            page['paging']['total'] = total
            page['paging']['first_url'] = self.node.paged_url(1, total)
            page['paging']['prev_url'] = self.node.paged_url(i - 1, total)
            page['paging']['next_url'] = self.node.paged_url(i + 1, total)
            page['paging']['last_url'] = self.node.paged_url(total, total)

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
        self.init()
        self.set_flag('is_leaf_index', True)
