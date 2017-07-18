#!/usr/bin/env python

import os
import sys

from pkg_resources import get_distribution, DistributionNotFound

try:
    get_distribution('fn')
    sys.stdout.write("""
{delimiter}
                   INSTALLATION ABORTED

The module "fn" was found on this system. Unfortunately
"fn.py" and "fn" cannot work together because they use the
same package name, i.e. fn. The "fn" module is no longer
maintained by the original author and "fn.py" is actually
a maintained fork of that project.

To complete this install, please uninstall "fn" (e.g.
pip uninstall fn) and rerun the installation of "fn.py".
{delimiter}
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
    name='fn.py',
    version=fn.__version__,
    description=short,
    long_description=(
        open('README.rst').read() +
        '\n\n' +
        open('CHANGELOG.rst').read()
    ),
    author='fnpy team',
    author_email='vash0the0stampede@gmail.com',
    url='https://github.com/fnpy/fn.py',
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ),
)
