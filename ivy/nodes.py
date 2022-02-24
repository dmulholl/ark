# ------------------------------------------------------------------------------
# This module is responsible for assembling and caching the parse tree of nodes.
# Each node corresponds to a text file and/or directory in the site's `src`
# directory. (A node file provides content and metadata for a node; a node
# directory stores child nodes.) Ivy parses the `src` directory into a tree of
# nodes which it then renders into a website, generating a single HTML page in
# the `out` directory for each node in the tree.
# ------------------------------------------------------------------------------

from __future__ import annotations
from typing import Dict, List, Callable, Any, Union, Optional
from pathlib import Path

import os
import sys

from . import utils
from . import events
from . import filters
from . import renderers
from . import site
from . import templates
from . import hashes


# Cached tree of Node instances.
_root = None


# Returns the site's root node. Parses the root directory and assembles the
# node tree when first called.
def root() -> Node:
    global _root
    if _root is None:
        if not os.path.isdir(site.src()):
            sys.exit("Error: cannot locate the site's source directory.")
        _root = Node()
        _parse_node_directory(_root, site.src())
    return _root


# Returns the node corresponding to the specified @root/ url if it exists,
# otherwise returns None.
def node(url: str) -> Optional[Node]:
    if url.startswith('@root/'):
        node = root()
        for slug in url.rstrip('/').split('/')[1:]:
            if (node := node.child(slug)) is None:
                break
        return node
    return None


# A Node instance represents a directory or text file (or both) in the
# site's source directory. You can treat a Node instance as a dictionary:
#
# >>> node = Node()
# >>> node['foo'] = 123
# >>> bar = node['foo']
#
# Dictionary-style reads and writes are passed through to the node's [.meta]
# dictionary.
class Node():

    def __init__(self):
        # Stores the node's metadata (title, author, date, etc.).
        self.meta: Dict[str, Any] = {}

        # Stores a reference to the node's parent node.
        self.parent: Optional[Node] = None

        # Stores child nodes.
        self.children: List[Node] = []

        # Stores the path to the node's source directory/file.
        # (The file path will overwrite the directory path if both exist.)
        self.filepath: str = ''

        # Stores the node's filepath stem, i.e. basename minus extension.
        self.stem: str = ''

        # Stores the node's filepath extension, stripped of its leading dot.
        self.ext: str = ''

        # Stores the node's raw text content.
        self.text: str = ''

        # Internal cache for generated data.
        self.cache: Dict[str, Any] = {}

    # Identifying nodes by their @root/ url is useful for debugging.
    def __repr__(self) -> str:
        return f"<Node {self.url}>"

    # Allows dictionary-style read access to the node's metadata.
    def __getitem__(self, key: str) -> Any:
        return self.meta[key]

    # Allows dictionary-style write access to the node's metadata.
    def __setitem__(self, key: str, value: Any):
        self.meta[key] = value

    # Dictionary-style 'in' support for metadata.
    def __contains__(self, key: str) -> bool:
        return key in self.meta

    # Dictionary-style 'get' support for metadata.
    def get(self, key: str, default: Any = None) -> Any:
        return self.meta.get(key, default)

    # Dictionary-style 'get' with inheritance for metadata. This method walks
    # its way up the ancestor chain looking for a matching entry.
    def inherit(self, key: str, default: Any = None) -> Any:
        while self is not None:
            if key in self.meta:
                return self.meta[key]
            self = self.parent
        return default

    # Calls the specified function on the node and all its descendants.
    def walk(self, callback):
        for node in self.children:
            node.walk(callback)
        callback(self)

    # Returns the node's path, i.e. the list of slugs which determines the node's
    # output filepath and url. (Returns a disposable copy of the cached list.)
    @property
    def path(self) -> List[str]:
        if not 'path' in self.cache:
            self.cache['path'] = []
            current = self
            while current.parent is not None:
                self.cache['path'].append(current.slug)
                current = current.parent
            self.cache['path'].reverse()
        return self.cache['path'].copy()

    # Returns the node's url.
    @property
    def url(self) -> str:
        if not 'url' in self.cache:
            if self.parent:
                self.cache['url'] = '@root/' + '/'.join(self.path) + '//'
            else:
                self.cache['url'] = '@root/'
        return self.cache['url']

    # True if the node has child nodes.
    @property
    def has_children(self) -> bool:
        return len(self.children) > 0

    # Returns the node's filepath/url slug.
    @property
    def slug(self) -> str:
        if not 'slug' in self.cache:
            self.cache['slug'] = self.meta.get('slug') or utils.slugify(self.stem)
        return self.cache['slug']

    # Returns the child node with the specified slug if it exists, otherwise None.
    def child(self, slug: str) -> Optional[Node]:
        for child in self.children:
            if child.slug == slug:
                return child
        return None

    # Returns the node's text content rendered into HTML. Note that the
    # `node_text` and `node_html` filters will only fire when this property
    # is first accessed, most likely by a {{ node.html }} reference in a
    # template file.
    @property
    def html(self) -> str:
        if not 'html' in self.cache:
            text = filters.apply('node_text', self.text, self)
            html = renderers.render(text, self.ext, self.filepath)
            self.cache['html'] = filters.apply('node_html', html, self)
        return self.cache['html']

    # Generates a HTML page for the node and writes that page to disk.
    def write(self):
        output_filepath = self.get_output_filepath()

        # This data dictionary gets passed to the template engine.
        page_data = {
            'node': self,
            'site': site.config,
            'inc': site.includes(),
            'is_homepage': self.parent is None,
            'filepath': output_filepath,
            'classes': self.get_class_list(),
            'templates': self.get_template_list(),
        }

        # Generate a HTML page by pouring the node's content into a template.
        events.fire(events.Event.RENDER_PAGE, page_data)
        page_html = templates.render(page_data)
        site.pages_rendered(1)

        # Filter the HTML before writing it to disk.
        page_html = filters.apply('page_html', page_html, page_data)

        # Rewrite all @root/ urls.
        page_html = utils.rewrite_urls(page_html, output_filepath)

        # Write the page to disk. Avoid overwriting identical files.
        if not hashes.match(output_filepath, page_html):
            utils.writefile(output_filepath, page_html)
            site.pages_written(1)

    # Returns the output filepath for the node.
    def get_output_filepath(self) -> str:
        slugs = self.path or ['index']
        suffix = site.config['extension']
        if suffix == '/':
            if slugs[-1] == 'index':
                slugs[-1] += '.html'
            else:
                slugs.append('index.html')
        else:
            slugs[-1] += suffix
        filepath = site.out(*slugs)
        return filters.apply('output_filepath', filepath, self)

    # Assembles an ordered list of hyphenated slugs for generating CSS classes
    # and running template lookups.
    # E.g. <Node @root/foo/bar//> -> ['node-foo-bar', 'node-foo', 'node'].
    def get_slug_list(self) -> List[str]:
        slugs = []
        stack = ['node'] + self.path
        while stack:
            slugs.append('-'.join(stack))
            stack.pop()
        return filters.apply('slug_list', slugs, self)

    # Assembles a list of potential template names for the node.
    def get_template_list(self) -> List[str]:
        template_list = self.get_slug_list()
        if 'template' in self.meta:
            template_list.insert(0, self.meta['template'])
        return filters.apply('template_list', template_list, self)

    # Assembles a list of CSS classes for the output page's <body> element.
    def get_class_list(self) -> List[str]:
        class_list = self.get_slug_list()
        if self.parent is None:
            class_list.append('homepage')
        if 'classes' in self.meta:
            for item in str(self.meta['classes']).split(','):
                class_list.append(item.strip())
        return filters.apply('class_list', class_list, self)


# Parse a source directory. The `load_node_dir` and `load_node_file` filters
# can be used as switches to determine if a directory or file should be treated
# as a node or ignored.
#
# Args:
#   dir_node (Node): the Node instance for the directory.
#   dir_path (str/Path): path to the directory as a string or Path instance.
def _parse_node_directory(dir_node, dir_path):

    # Parse subdirectories.
    for subdir_path in (p for p in Path(dir_path).iterdir() if p.is_dir()):
        if filters.apply('load_node_dir', True, subdir_path):
            child_node = Node()
            child_node.stem = subdir_path.stem
            child_node.parent = dir_node
            child_node.filepath = str(subdir_path)
            dir_node.children.append(child_node)
            _parse_node_directory(child_node, subdir_path)

    # Parse files.
    for file_path in (p for p in Path(dir_path).iterdir() if p.is_file()):
        if file_path.stem.startswith('.') or file_path.stem.endswith('~'):
            continue
        if filters.apply('load_node_file', True, file_path):
            _parse_node_file(dir_node, file_path)


# Parse a source file.
#
# Args:
#   dir_node (Node): the Node instance for the directory containing the file.
#   file_path (Path): path to the file as a Path instance.
def _parse_node_file(dir_node, file_path):
    if file_path.stem == 'index':
        file_node = dir_node
    else:
        file_node = None
        for child in dir_node.children:
            if file_path.stem == child.stem:
                file_node = child
                break
        if file_node is None:
            file_node = Node()
            file_node.stem = file_path.stem
            file_node.parent = dir_node
            dir_node.children.append(file_node)
    text, meta = utils.loadfile(file_path)
    file_node.text = text
    file_node.meta.update(meta)
    file_node.filepath = str(file_path)
    file_node.ext = file_path.suffix.strip('.')
