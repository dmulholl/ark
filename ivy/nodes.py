# ------------------------------------------------------------------------------
# This module creates and caches the parse-tree of Node instances.
# ------------------------------------------------------------------------------

from . import utils
from . import hooks
from . import renderers
from . import loader
from . import site

from pathlib import Path
from typing import Dict, List, Callable, Any, Union
from typing import Optional as Opt


# Cached parse tree of Node instances.
_root: Opt['Node'] = None


# A Node instance represents a directory or text file (or both) in the
# site's source directory.
class Node():

    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.parent: Opt['Node'] = None
        self.children: Dict[str, 'Node'] = {}
        self.stem: str = ''
        self.slug: str = ''
        self.ext: str = ''
        self.empty: bool = True

        # Default attributes.
        self['text'] = ''
        self['html'] = ''

    # String representation of the Node instance.
    def __repr__(self) -> str:
        return "<Node /%s>" % '/'.join(self.path)

    # Dictionary-style read access.
    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    # Dictionary-style write access.
    def __setitem__(self, key: str, value: Any):
        self.data[key] = value

    # Dictionary-style 'in' support.
    def __contains__(self, key: str) -> bool:
        return key in self.data

    # Dictionary-style 'get' support.
    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    # Dictionary-style 'get' with attribute inheritance.
    def inherit(self, key: str, default: Any = None) -> Any:
        while self is not None:
            if key in self.data:
                return self.data[key]
            self = self.parent
        return default

    # Dictionary-style 'update' support.
    def update(self, other: Dict[str, Any]):
        self.data.update(other)

    # Return a printable tree showing the node and its descendants.
    def str(self, depth: int = 0) -> str:
        out = ["·  " * depth + '/' + '/'.join(self.path)]
        for child in self.childlist:
            out.append(child.str(depth + 1))
        return '\n'.join(out)

    # Initialize the node. This method is called on the root node once the
    # parse tree has been assembled. It recursively calls itself on all
    # subnodes.
    def init(self) -> 'Node':

        # Filter the node's text on the 'node_text' hook.
        self['text'] = hooks.filter('node_text', self['text'], self)

        # Render the filtered text into html.
        html = renderers.render(self['text'], self.ext)

        # Filter the node's html on the 'node_html' hook.
        self['html'] = hooks.filter('node_html', html, self)

        # Initialize any subnodes.
        for node in self.children.values():
            node.init()

        # Fire the 'init_node' event. This fires 'bottom up', i.e. when this
        # event fires on a node, all its descendants have already been
        # initialized.
        hooks.event('init_node', self)

        # Enable chaining.
        return self

    # Call the specified function on the node and all its descendants.
    def walk(self, callback: Callable[['Node'], None]):
        for node in self.children.values():
            node.walk(callback)
        callback(self)

    # Returns the node's path, i.e. the list of slugs that uniquely identify
    # its location in the parse tree.
    @property
    def path(self) -> List[str]:
        slugs = []
        while self.parent is not None:
            slugs.append(self.slug)
            self = self.parent
        slugs.reverse()
        return slugs

    # Returns the node's url.
    @property
    def url(self) -> str:
        if self.parent:
            return '@root/' + '/'.join(self.path) + '//'
        else:
            return '@root/'

    # Returns a list of child nodes ordered by stem.
    @property
    def childlist(self) -> List['Node']:
        return [self.children[stem] for stem in sorted(self.children)]

    # True if the node has child nodes.
    @property
    def has_children(self) -> bool:
        return len(self.children) > 0


# Returns the site's root node. Parses the root directory and assembles the
# node tree on first call.
def root() -> Node:
    global _root
    if _root is None:
        _root = Node()
        _parse_node_directory(_root, site.src())
        hooks.event('init_tree', _root.init())
    return _root


# Returns the node corresponding to the specified path, i.e. the sequence of
# slugs that uniquely identifies the node in the parse tree. Returns None if the
# node does not exist.
def node(*slugs: str) -> Opt[Node]:
    node = root()
    for slug in slugs:
        if not slug in node.children:
            return None
        node = node.children[slug]
    return node


# Parse a source directory.
#
# Args:
#   dirnode (Node): the Node instance for the directory.
#   dirpath (str/Path): path to the directory as a string or Path instance.
def _parse_node_directory(dirnode: Node, dirpath: Union[str, Path]):

    # Loop over the directory's subdirectories.
    for path in [p for p in Path(dirpath).iterdir() if p.is_dir()]:
        slug = utils.slugify(path.stem)
        childnode = Node()
        childnode.slug = slug
        childnode.stem = path.stem
        childnode.parent = dirnode
        dirnode.children[slug] = childnode
        _parse_node_directory(childnode, path)

    # Loop over the directory's files. We skip dotfiles and file types for
    # which we don't have a registered rendering-engine callback.
    for path in [p for p in Path(dirpath).iterdir() if p.is_file()]:
        if path.stem.startswith('.'):
            continue
        if not renderers.is_registered_ext(path.suffix.strip('.')):
            continue
        _parse_node_file(dirnode, path)


# Parse a source file.
#
# Args:
#   dirnode (Node): the Node instance for the directory containing the file.
#   filepath (Path): path to the file as a Path instance.
def _parse_node_file(dirnode: Node, filepath: Path):

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
        dirnode.children[slug] = filenode

    # Update the new or existing node with the file's text and metadata.
    filenode['text'], meta = loader.load(filepath)
    filenode.update(meta)

    # The file's extension determines the rendering engine we use to
    # transform its text into html.
    filenode.ext = filepath.suffix.strip('.')

    # Flip the empty bit so we know this node has content.
    filenode.empty = False
