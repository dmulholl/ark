# ------------------------------------------------------------------------------
# This module creates and caches the parse-tree of Node instances.
# ------------------------------------------------------------------------------

from __future__ import annotations
from typing import Dict, List, Callable, Any, Union, Optional
from pathlib import Path

from . import utils
from . import events
from . import filters
from . import renderers
from . import loader
from . import site


# Cached parse tree of Node instances.
_root: Optional[Node] = None


# Returns the site's root node. Parses the root directory and assembles the
# node tree on first call.
def root() -> Node:
    global _root
    if _root is None:
        _root = Node()
        _parse_node_directory(_root, site.src())
        _root.init()
        events.fire('init_tree', _root)
    return _root


# Returns the node corresponding to the specified url if it exists.
def node(url: str) -> Optional[Node]:
    if not url.startswith('@root/'):
        return None
    node = root()
    for slug in url.rstrip('/').split('/')[1:]:
        if (node := node.child(slug)) is None:
            break
    return node


# A Node instance represents a directory or text file (or both) in the
# site's source directory.
class Node():

    def __init__(self):

        # Stores the node's metadata (title, subtitle, author, etc.).
        self.meta: Dict[str, Any] = {}

        # Stores a reference to the node's parent node.
        self.parent: Optional[Node] = None

        # Stores child nodes.
        self.children: List[Node] = []

        # Stores the filepath of the node's source file.
        self.filepath: str = ''

        # Stores the node's filepath stem, i.e. basename minus extension.
        self.stem: str = ''

        # Stores the node's filepath extension, stripped of its leading dot.
        self.ext: str = ''

        # Stores the node's raw text content.
        self.text: str = ''

        # Stores the node's processed html content.
        self.html: str = ''

    # String representation of the Node instance.
    def __repr__(self) -> str:
        return f"<Node {self.url}>"

    # Allow dictionary-style read access to the node's metadata.
    def __getitem__(self, key: str) -> Any:
        return self.meta[key]

    # Allow dictionary-style write access to the node's metadata.
    def __setitem__(self, key: str, value: Any):
        self.meta[key] = value

    # Dictionary-style 'in' support for metadata.
    def __contains__(self, key: str) -> bool:
        return key in self.meta

    # Dictionary-style 'get' support for metadata.
    def get(self, key: str, default: Any = None) -> Any:
        return self.meta.get(key, default)

    # Dictionary-style 'get' with inheritance for metadata.
    def inherit(self, key: str, default: Any = None) -> Any:
        while self is not None:
            if key in self.meta:
                return self.meta[key]
            self = self.parent
        return default

    # Dictionary-style 'update' support for metadata.
    def update(self, other: Dict[str, Any]):
        self.meta.update(other)

    # Returns a printable tree showing the node and its descendants.
    def tree(self, depth: int = 0, urls: bool = True) -> str:
        out = ["·  " * depth + self.url] if urls else ["·  " * depth + self.slug or '/']
        for child in self.children:
            out.append(child.tree(depth + 1, urls))
        return '\n'.join(out)

    # This method should be called on a new node after its metadata and .text
    # attributes have been assigned. It initializes the node by filtering its
    # text and rendering it into html. Calling this method on the root node of
    # a tree will automatically initialize all descendant nodes. (In this case
    # the filter and event hooks fire 'bottom up', i.e. when they fire on a
    # node, all its decendents have already been initialized.)
    def init(self):
        for node in self.children:
            node.init()
        self.text = filters.apply('node_text', self.text, self)
        html = renderers.render(self.text, self.ext, self.filepath)
        self.html = filters.apply('node_html', html, self)
        events.fire('init_node', self)

    # Call the specified function on the node and all its descendants.
    def walk(self, callback: Callable[['Node'], None]):
        for node in self.children:
            node.walk(callback)
        callback(self)

    # Returns the node's path, i.e. the list of slugs that determine its output
    # filepath and url.
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

    # True if the node has child nodes.
    @property
    def has_children(self) -> bool:
        return len(self.children) > 0

    # Returns the node's filepath/url slug.
    @property
    def slug(self) -> str:
        return self.meta.get('slug') or utils.slugify(self.stem)

    # Returns the child node with the specified slug if it exists, otherwise None.
    def child(self, slug: str) -> Optional[Node]:
        for child in self.children:
            if child.slug == slug:
                return child
        return None


# Parse a source directory.
#
# Args:
#   dirnode (Node): the Node instance for the directory.
#   dirpath (str/Path): path to the directory as a string or Path instance.
def _parse_node_directory(dirnode: Node, dirpath: Union[str, Path]):

    # Loop over the directory's subdirectories.
    for path in (p for p in Path(dirpath).iterdir() if p.is_dir()):
        childnode = Node()
        childnode.stem = path.stem
        childnode.parent = dirnode
        childnode.filepath = str(path)
        dirnode.children.append(childnode)
        _parse_node_directory(childnode, path)

    # Loop over the directory's files. We skip dotfiles and file types for
    # which we don't have a registered rendering-engine callback.
    for path in (p for p in Path(dirpath).iterdir() if p.is_file()):
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
    if filepath.stem == 'index':
        filenode = dirnode
    else:
        filenode = None
        for child in dirnode.children:
            if filepath.stem == child.stem:
                filenode = child
                break
        if filenode is None:
            filenode = Node()
            filenode.stem = filepath.stem
            filenode.parent = dirnode
            dirnode.children.append(filenode)
    text, meta = loader.load(filepath)
    filenode.text = text
    filenode.update(meta)
    filenode.filepath = str(filepath)
    filenode.ext = filepath.suffix.strip('.')
