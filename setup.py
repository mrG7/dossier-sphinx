#!/usr/bin/env python
from __future__ import absolute_import
from setuptools import setup
from distutils.command.install_data import install_data
from version import get_git_version

import os
import os.path as path

VERSION, SOURCE_HASH = get_git_version()
PROJECT = 'dossier-sphinx'
URL = 'http://github.com/dossier'
AUTHOR = 'Diffeo, Inc.'
AUTHOR_EMAIL = 'support@diffeo.com'
DESC = 'Master Dossier documentation set.'
LICENSE = open(path.join(path.dirname(__file__), 'LICENSE')).read()

def subtree(t, d):
    for dirpath, dirnames, filenames in os.walk(d):
        yield (os.path.join(t, os.path.relpath(dirpath, d)),
               [os.path.join(dirpath, filename) for filename in filenames])

class install_data_sphinx(install_data):
    def run(self):
        self.run_command('build_sphinx')
        self.data_files.remove('MARKER.txt')
        sphinx = self.get_finalized_command('build_sphinx')
        self.data_files += list(subtree('docs/html',
                                        os.path.join(sphinx.build_dir, 'html')))
        install_data.run(self)

setup(
    name=PROJECT,
    version=VERSION,
    license=LICENSE,
    description=DESC,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    cmdclass={'install_data': install_data_sphinx},

    install_requires=[
        'docutils',
        'Sphinx',
        'sphinxcontrib-httpdomain',
        'dossier.fc',
        'dossier.store',
    ],
    # there must be a data_files for install_data to run
    data_files=['MARKER.txt'],
)
