# coding=utf-8
"""
setup file
"""
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

localdir = os.path.dirname(os.path.abspath(__file__))
name = 'stopwatch-multiclock'
pkg = __import__('StopWatch')

author, email = pkg.__author__.rsplit(' ', 1)
email = email.strip('<>')

version = pkg.__version__

readme = open(os.path.join(localdir, 'README.md'), 'r').readlines()
description = readme[5]
long_description = ''.join(readme)

setup(
        name='StopWatch',
        version=version,
        packages=['tests', 'StopWatch'],
        url='https://github.com/cyclops3590/StopWatch',
        download_url='https://github.com/cyclops3590/StopWatch',
        license='BSD',
        author=author,
        author_email=email,
        description='Multiclock Stopwatch',
        requires=['unittest2'],
        keywords=['stopwatch', 'multi-clock'],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            "Programming Language :: Python :: 2",
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Operating System :: OS Independent'
        ],
        zip_safe=True,
        platforms=['MacOS', 'POSIX'],
        maintainer=author,
        maintainer_email=email,
        provides=['StopWatch']
)
