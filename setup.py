#!/usr/bin/env python3
"""
Ivy
===

Ivy is a static website generator. It transforms a directory of text files into
a self-contained website.

* `Documentation <http://www.dmulholl.com/docs/ivy/>`_

"""

import os
import re
import io

from setuptools import setup, find_packages


# MANIFEST.in file content.
manifest = """\
include license.txt readme.md
recursive-include ivy/extensions *
recursive-include ivy/initsite *
"""


# Write a temporary MANIFEST.in file alongside the setup.py file.
manpath = os.path.join(os.path.dirname(__file__), 'MANIFEST.in')
with io.open(manpath, 'w', encoding='utf-8') as manfile:
    manfile.write(manifest)


# Load the package's metadata into the meta dict.
metapath = os.path.join(os.path.dirname(__file__), 'ivy', '__init__.py')
with io.open(metapath, encoding='utf-8') as metafile:
    regex = r'''^__([a-z]+)__ = ["'](.*)["']'''
    meta = dict(re.findall(regex, metafile.read(), flags=re.MULTILINE))


# Standard setup routine.
setup(
    name = 'ivy',
    version = meta['version'],
    packages =  find_packages(),
    include_package_data = True,
    entry_points = {
        'console_scripts': [
            'ivy = ivy:main',
        ],
    },
    install_requires = [
        'markdown ~= 3.0.0',
        'pygments ~= 2.0.0',
        'pyyaml ~= 5.0',
        'jinja2 ~= 2.0',
        'syntext ~= 2.0.0',
        'libjanus ~= 1.0.0',
        'ibis ~= 1.6.0',
        'shortcodes ~= 2.5.0',
        'colorama ~= 0.4',
    ],
    author = 'Darren Mulholland',
    url='http://www.dmulholl.com/docs/ivy/',
    license = 'Public Domain',
    description = 'A static website generator.',
    long_description = __doc__,
    classifiers = [
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: Public Domain',
        'Topic :: Text Processing :: Markup :: HTML',
    ],
)


# Delete the temporary MANIFEST.in file.
if os.path.isfile(manpath):
    os.remove(manpath)
