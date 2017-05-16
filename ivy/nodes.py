# --------------------------------------------------------------------------
# This module creates and caches the parse-tree of Node instances.
# --------------------------------------------------------------------------

import pathlib

from . import utils
from . import hooks
from . import renderers
from . import loader
from . import site


# Stores the parse tree of Node instances.
cache = None


# Return the site's root node. Parses the root directory and assembles the
# node tree on first call.
def root():
    global cache
    if cache is None:
        cache = Node()
        parse_node_directory(cache, site.src())
        hooks.event('init_tree', cache.init())
    return cache


# Return the node corresponding to the specified path, i.e. the sequence of
# slugs uniquely identifying the node in the parse tree. Returns None if the
# node does not exist.
def node(*slugs):
    node = root()
    for slug in slugs:
        if not slug in node.subnodes:
            return None
        node = node.subnodes[slug]
    return node


# A Node instance represents a directory or text file (or both) in the
# site's source directory.
class Node():

    def __init__(self):
        self.data = {}
        self.parent = None
        self.subnodes = {}
        self.stem = ''
        self.slug = ''
        self.format = ''

        # Default attributes.
        self['text'] = ''
        self['html'] = ''

    # String representation of the Node instance.
    def __repr__(self):
        return "<Node /%s>" % '/'.join(self.path)

    # Dictionary-style read access.
    def __getitem__(self, key):
        return self.data[key]

    # Dictionary-style write access.
    def __setitem__(self, key, value):
        self.data[key] = value

    # Dictionary-style 'in' support.
    def __contains__(self, key):
        return key in self.data

    # Dictionary-style 'get' support.
    def get(self, key, default=None):
        return self.data.get(key, default)

    # Dictionary-style 'get' with attribute inheritance.
    def inherit(self, key, default=None):
        while self is not None:
            if key in self.data:
                return self.data[key]
            self = self.parent
        return default

    # Dictionary-style 'update' support.
    def update(self, other):
        self.data.update(other)

    # Return a printable tree showing the node and its descendants.
    def str(self, depth=0):
        out = ["·  " * depth + '/' + '/'.join(self.path)]
        for child in self.children:
            out.append(child.str(depth + 1))
        return '\n'.join(out)

    # Initialize the node. This method is called on each node in the parse
    # tree once the entire tree has been assembled.
    def init(self):

        # Filter the node's text on the 'node_text' hook.
        self['text'] = hooks.filter('node_text', self['text'], self)

        # Render the filtered text into html.
        html = renderers.render(self['text'], self.format)

        # Filter the node's html on the 'node_html' hook.
        self['html'] = hooks.filter('node_html', html, self)

        # Initialize the node's subnodes.
        for node in self.subnodes.values():
            node.init()

        # Fire the 'init_node' event. This fires 'bottom up', i.e. when this
        # event fires on a node, all its subnodes have already been
        # initialized.
        hooks.event('init_node', self)

        # Enable chaining.
        return self

    # Call the specified function on the node and all its descendants.
    def walk(self, callback):
        for node in self.subnodes.values():
            node.walk(callback)
        callback(self)

    # Return the node's path, i.e. the list of slugs that uniquely identify
    # its location in the parse tree.
    @property
    def path(self):
        slugs = []
        while self.parent is not None:
            slugs.append(self.slug)
            self = self.parent
        slugs.reverse()
        return slugs

    # Return the node's url.
    @property
    def url(self):
        if self.parent:
            return '@root/' + '/'.join(self.path) + '//'
        else:
            return '@root/'

    # Return a list of child nodes ordered by slug.
    @property
    def children(self):
        return [self.subnodes[slug] for slug in sorted(self.subnodes)]

    # Return a list of descendent nodes. (Undefined order.)
    @property
    def descendants(self):
        descendent_nodes = []
        for subnode in self.subnodes.values():
            descendent_nodes.append(subnode)
            descendent_nodes.extend(subnode.descendants)
        return descendent_nodes

    # Return a list of descendent leaf nodes. (Undefined order)
    @property
    def leaves(self):
        leaf_nodes = []
        for subnode in self.subnodes.values():
            if subnode.subnodes:
                leaf_nodes.extend(subnode.leaves)
            else:
                leaf_nodes.append(subnode)
        return leaf_nodes


# Parse a source directory.
#
# Args:
#   dirnode (Node): the Node instance for the directory.
#   dirpath (str/Path): path to the directory as a string or Path instance.
def parse_node_directory(dirnode, dirpath):

    # Loop over the directory's subdirectories.
    for path in [p for p in pathlib.Path(dirpath).iterdir() if p.is_dir()]:
        slug = utils.slugify(path.stem)
        subnode = Node()
        subnode.slug = slug
        subnode.stem = path.stem
        subnode.parent = dirnode
        dirnode.subnodes[slug] = subnode
        parse_node_directory(subnode, path)

    # Loop over the directory's files. We skip dotfiles and file types for
    # which we don't have a registered rendering-engine callback.
    for path in [p for p in pathlib.Path(dirpath).iterdir() if p.is_file()]:
        if path.stem.startswith('.'):
            continue
        if path.suffix.strip('.') not in renderers.callbacks:
            continue
        parse_node_file(dirnode, path)


# Parse a source file.
#
# Args:
#   dirnode (Node): the Node instance for the directory containing the file.
#   filepath (Path): path to the file as a Path instance.
def parse_node_file(dirnode, filepath):

    # Check if the file is coterminous with an existing node before creating
    # a new one.
    slug = utils.slugify(filepath.stem)
    if slug == 'index':
        filenode = dirnode
    else:
        filenode = node(*dirnode.path, slug) or Node()
        filenode.slug = slug
        filenode.stem = filepath.stem
        filenode.parent = dirnode
        dirnode.subnodes[slug] = filenode

    # Update the new or existing node with the file's text and metadata.
    filenode['text'], meta = loader.load(filepath)
    filenode.update(meta)

    # The file's extension determines the rendering engine we use to
    # transform its text into html.
    filenode.format = filepath.suffix.strip('.')
