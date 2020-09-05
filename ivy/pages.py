# ------------------------------------------------------------------------------
# This module renders and writes HTML pages to disk.
# ------------------------------------------------------------------------------

import re
import os

from . import site
from . import events
from . import filters
from . import utils
from . import templates
from . import hashes

from typing import List
from .nodes import Node


# A Page instance represents a single HTML page in the rendered site.
class Page(dict):

    # Each Page is initialized with an associated Node instance. This node's
    # location in the parse tree determines the output filepath for the page.
    def __init__(self, node: Node):
        self['node'] = node
        self['site'] = site.config
        self['inc'] = site.includes()
        self['is_homepage'] = node.parent is None

    # Render the page into HTML and write the HTML to disk.
    def write(self):
        self['filepath'] = self.get_filepath()
        self['classes'] = self.get_class_list()
        self['templates'] = self.get_template_list()

        # Render the page into HTML.
        events.fire('render_page', self)
        html = templates.render(self)
        site.rendered(1)

        # Filter the HTML before writing it to disk.
        html = filters.apply('page_html', html, self)

        # Rewrite all @root/ urls.
        html = utils.rewrite_urls(html, self['filepath'])

        # Write the page to disk. Avoid overwriting identical files.
        if not hashes.match(self['filepath'], html):
            utils.writefile(self['filepath'], html)
            site.written(1)

    # Determine the output filepath for the page.
    def get_filepath(self) -> str:
        slugs = self['node'].path or ['index']
        suffix = site.config['extension']
        if suffix == '/':
            if slugs[-1] == 'index':
                slugs[-1] += '.html'
            else:
                slugs.append('index.html')
        else:
            slugs[-1] += suffix
        filepath = site.out(*slugs)
        return filters.apply('page_path', filepath, self)

    # Assemble an ordered list of hyphenated slugs for generating CSS classes
    # and running template lookups.
    # E.g. <Node @root/foo/bar//> -> ['node-foo-bar', 'node-foo', 'node'].
    def get_slug_list(self) -> List[str]:
        slugs = []
        stack = ['node'] + self['node'].path
        while stack:
            slugs.append('-'.join(stack))
            stack.pop()
        return filters.apply('page_slugs', slugs, self)

    # Assemble a list of potential template names for the page.
    def get_template_list(self) -> List[str]:
        template_list = self.get_slug_list()
        if 'template' in self['node']:
            template_list.insert(0, self['node']['template'])
        return filters.apply('page_templates', template_list, self)

    # Assemble a list of CSS classes for the page's <body> element.
    def get_class_list(self) -> List[str]:
        class_list = self.get_slug_list()
        if self['is_homepage']:
            class_list.append('homepage')
        if 'classes' in self['node']:
            for item in str(self['node']['classes']).split(','):
                class_list.append(item.strip())
        return filters.apply('page_classes', class_list, self)
