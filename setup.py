#!/usr/bin/env python

import os
import sys

from pkg_resources import get_distribution, DistributionNotFound

try:
    get_distribution('fn')
    get_distribution('fn.py')
    sys.stdout.write("""
{delimiter}
                   INSTALLATION ABORTED

One of the modules "fn" or "fn.py" were found on this system. 
Unfortunately "fn.py" and "fn" cannot work together because 
they use the same package name. This project is a fork of "fn.py"
""".format(delimiter='=' * 60))
    sys.exit(0)
except DistributionNotFound:
    pass

import fn

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

short = '''
Implementation of missing features to enjoy functional programming in Python
'''
setup(
    name='fn-mdowds',
    version=fn.__version__,
    description=short,
    long_description=(
        open('README.rst').read() +
        '\n\n' +
        open('CHANGELOG.rst').read()
    ),
    author='fnpy team',
    url='https://github.com/mdowds/fn.py',
    packages=['fn', 'fn.immutable'],
    package_data={'': ['LICENSE', 'README.rst', 'CHANGELOG.rst']},
    include_package_data=True,
    install_requires=[],
    license=open('LICENSE').read(),
    zip_safe=False,
    keywords=['functional', 'fp', 'utility'],
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ),
)
