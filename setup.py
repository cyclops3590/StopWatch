# coding=utf-8
"""
setup file
"""
import os
from distutils.core import setup

localdir = os.path.dirname(os.path.abspath(__file__))
name = 'stopwatch-multiclock'
pkg = __import__('stopwatch')

author, email = pkg.__author__.rsplit(' ', 1)
email = email.strip('<>')

version = pkg.__version__

readme = open(os.path.join(localdir, 'README.md'), 'r').readlines()
description = readme[5]
long_description = ''.join(readme)

try:
    test_reqs = open(os.path.join(os.path.dirname(__file__), 'test_requirements.txt')).read()
except (IOError, OSError):
    test_reqs = reqs = ''


setup(
        name='StopWatch',
        version='0.3.0',
        packages=['tests', 'StopWatch'],
        url='https://github.com/cyclops3590/StopWatch',
        license='None',
        author='cyclops',
        author_email='cyclops3590@gmail.com',
        description='Multiclock Stopwatch', requires=['unittest2']
)
