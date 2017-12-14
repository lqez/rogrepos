#!/usr/bin/env python
from setuptools import setup, find_packages
import re

with open('rogrepos/__init__.py') as f:
    data = re.search(r'\(\s*(\d*).\s*(\d*).\s*(\d)*\)', f.read())
    version = ".".join([data.group(1), data.group(2), data.group(3)])
assert version

classifiers = [
    'Topic :: Terminals',
    'Topic :: Utilities',
    'Environment :: Console',
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python',
    'License :: OSI Approved :: MIT License',
]

setup(
    name='rogrepos',
    version='0.1.0',
    packages=find_packages('.'),
    zip_safe=True,
    author='Park Hyunwoo',
    author_email='ez.amiryo' '@' 'gmail.com',
    maintainer='Park Hyunwoo',
    maintainer_email='ez.amiryo' '@' 'gmail.com',
    url='http://github.com/lqez/rogrepos',
    description='Rogrepos removes outdated GitHub repositories',
    classifiers=classifiers,
    entry_points={
        'console_scripts': [
            'rogrepos = rogrepos.rogrepos:rogrepos',
        ],
    },
)
