# --------------------------------------------------------------------------
# This extension adds support for user-defined tags. Tags can be added to a
# node as a comma-separated list via a 'tags' attribute.
# --------------------------------------------------------------------------

from ivy import hooks, nodes, slugs, indexes


# A Tag instance pairs a tag-name with its corresponding tag-index url.
class Tag:

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return 'Tag(name=%s, url=%s)' % (repr(self.name), repr(self.url))

    def __str__(self):
        return '<a href="%s">%s</a>' % (self.url, self.name)


# Register a callback on the 'init_node' event hook to process each newly
# initialized node's tags. If the node has a 'tags' attribute, we convert
# each tagname in its comma-separated list into a Tag instance.
@hooks.register('init_node')
def register_tags(node):
    tagstring, node['tags'] = str(node.data.get('tags', '')), []
    for name in (name.strip() for name in tagstring.split(',')):
        if name:
            node['tags'].append(Tag(name, tag_index_url(node, name)))


# Return the tag-index url for the specified tag. The tag index is located
# at the closest ancestor node with a 'tagged' attribute.
def tag_index_url(node, tagname):
    while node is not None:
        if node.data.get('tagged'):
            return node.index_url(
                node.get('tag_slug', 'tags'), slugs.slugify(tagname))
        node = node.parent
    return ''


# A TagIndex lists all a node's descendants with a particular tag.
class TagIndex(indexes.Index):

    def __init__(self, node, nodes):
        super().__init__(node, nodes, node.get('per_tag_index'))
        self.set_flag('is_tag_index', True)


# Walk the parse tree and build tag indexes where required.
@hooks.register('main_build')
def build_tag_indexes():
    nodes.root().walk(node_callback)


# If a node (/node) has the 'tagged' attribute, we create a phantom 'tags'
# node just below it (/node/tags), and then a phantom tag-index node
# (/node/tags/tagname) for each individual tag found among the original
# node's descendants.
def node_callback(node):
    if node.data.get('tagged'):
        tags_node = nodes.Node()
        tags_node.parent = node
        tags_node.slug = node.get('tag_slug', 'tags')

        tag_map = {}
        for descendant in node.descendants():
            if 'tags' in descendant.data:
                for tag_obj in descendant.data['tags']:
                    tag_map.setdefault(tag_obj.name, []).append(descendant)

        for tag_name, tag_list in tag_map:
            tag_node = nodes.Node()
            tag_node.parent = tags_node
            tag_node.slug = slugs.slugify(tag_name)
            tag_node['title'] = tag_name

            TagIndex(tag_node, tag_list).render()
