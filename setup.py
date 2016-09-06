#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://osobotsu.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='osobotsu',
    version='0.1.0',
    description='a thing i guess',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Several Otters',
    author_email='theemagicwords@gmail.com',
    url='https://github.com/theemagicwords/osobotsu',
    packages=[
        'osobotsu',
    ],
    package_dir={'osobotsu': 'osobotsu'},
    include_package_data=True,
    install_requires=[
    ],
    license='OSL',
    zip_safe=False,
    keywords='osobotsu',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Reprobates',
        'License :: Entirely Made Up :: OSL',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
