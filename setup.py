# -*- coding: utf-8 -*-
"""
confprops setup.py

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
from codecs import open
from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='UTF-8') as f:
    long_description = f.read()

setup(
    # https://packaging.python.org/specifications/core-metadata/#name
    name='confprops',
    # https://www.python.org/dev/peps/pep-0440/
    version='0.1.0',
    # https://packaging.python.org/specifications/core-metadata/#summary
    description='Java like properties for configuration',
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=long_description,
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    url='https://github.com/pypa/sampleproject',
    author='Bhathiya Perera',
    author_email='bhathiya91@live.com',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='config java properties property file',
    packages=find_packages(include='confprops')
)
