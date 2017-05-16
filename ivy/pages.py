# --------------------------------------------------------------------------
# This module renders and writes html pages to disk.
# --------------------------------------------------------------------------

import re
import os

from . import site
from . import includes
from . import hooks
from . import utils
from . import templates
from . import hashes


# A Page instance represents a single html page in the rendered site.
class Page(dict):

    # Every Page is initialized with an associated Node instance. This
    # node's location in the parse tree determines the page's output path.
    def __init__(self, node):
        self['inc'] = includes.load()
        self['site'] = site.config
        self['node'] = node
        self['flags'] = {'is_homepage': node.parent is None}

    # Render the page into html and write the html to disk.
    def render(self):

        # Fire the 'render_page' event.
        hooks.event('render_page', self)

        # Determine the output filepath.
        self['filepath'] = self.get_filepath()

        # Generate a string of CSS classes for the page.
        self['classes'] = ' '.join(self.get_class_list())

        # Generate a list of potential template names.
        self['templates'] = self.get_template_list()

        # Render the page into html.
        html = templates.render(self)
        site.rendered(1)

        # Filter the html before writing it to disk.
        html = hooks.filter('page_html', html, self)

        # Rewrite all @root/ urls.
        html = self.rewrite_urls(html)

        # Write the page to disk. Avoid overwriting identical files.
        if not hashes.match(self['filepath'], html):
            utils.writefile(self['filepath'], html)
            site.written(1)

    # Determine the output filepath for the page.
    def get_filepath(self):
        slugs = self['node'].path or ['index']
        suffix = site.config['extension']

        if suffix == '/':
            if slugs[-1] == 'index':
                slugs[-1] += '.html'
            else:
                slugs.append('index.html')
        else:
            slugs[-1] += suffix

        return hooks.filter('page_path', site.out(*slugs), self)

    # Regex for locating @root/ urls for rewriting. Note that we only
    # rewrite urls enclosed in quotes or angle brackets.
    re_url = re.compile(r'''(["'<])@root/(.*?)(#.*?)?(\1|>)''')

    # Rewrite @root/ urls to their final form.
    def rewrite_urls(self, html):
        relpath = os.path.relpath(self['filepath'], site.out())
        depth = len(relpath.replace('\\', '/').split('/'))

        prefix = site.config.get('root') or '../' * (depth - 1)
        suffix = site.config.get('extension')

        # Each matched url is replaced with the output of this callback.
        def callback(match):
            quote = match.group(1) if match.group(1) in ('"', "'") else ''
            url = match.group(2).lstrip('/')
            fragment = match.group(3) or ''

            # The link points to the homepage.
            if url == '':
                if suffix == '/':
                    if depth == 1:
                        url = '' if fragment else '#'
                    else:
                        url = prefix
                else:
                    url = prefix + 'index' + suffix

            # The link points to a node page.
            elif url.endswith('//'):
                if suffix == '/':
                    url = prefix + url.strip('/') + '/'
                else:
                    url = prefix + url.strip('/') + suffix

            # The link points to a static asset or directory.
            else:
                url = prefix + url

            # Assemble the url inside its original quotes.
            return '%s%s%s%s' % (quote, url, fragment, quote)

        # Replace each match with the return value of the callback.
        return self.re_url.sub(callback, html)

    # Assemble a list of path slugs.
    def get_slug_list(self):
        slugs, stack = [], ['node'] + self['node'].path

        while stack:
            slugs.append('-'.join(stack))
            stack.pop()

        return hooks.filter('page_slugs', slugs, self)

    # Assemble a list of potential template names for the page.
    def get_template_list(self):
        template_list = self.get_slug_list()

        if 'template' in self['node']:
            template_list.insert(0, self['node']['template'])

        return hooks.filter('page_templates', template_list, self)

    # Assemble a list of CSS classes for the page's <body> element.
    def get_class_list(self):
        class_list = self.get_slug_list()

        if 'classes' in self['node']:
            for item in str(self['node']['classes']).split(','):
                class_list.append(item.strip())

        return hooks.filter('page_classes', class_list, self)
