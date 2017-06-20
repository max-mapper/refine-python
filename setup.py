#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

long_description = """
This allows you to script Refine by creating projects from data files, applying extracted JSON operation histories against the data and then exporting the transformed data back out of Refine.
"""

def get_install_requires():
    """
    parse requirements.txt, ignore links, exclude comments
    """
    requirements = []
    for line in open('requirements.txt').readlines():
        line = line.rstrip()
        # skip to next iteration if comment or empty line
        if any([line.startswith('#'), line == '', line.startswith('http'), line.startswith('git'), line == '-r base.txt']):
            continue
        # add line to requirements
        requirements.append(line)
    return requirements

setup(
    name='refine',
    version='0.1',
    packages=['refine'],
    entry_points={
        'console_scripts': ['refine-cli = refine:main']},
    install_requires=get_install_requires(),
    # metadata for upload to PyPI
    author="David Huynh",
    author_email="",
    description=("Python client library for Google Refine"),
    license='MIT',
    keywords=['OpenRefine', 'CSV', 'data'],
    url='https://github.com/PabloCastellano/refine-python',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Text Processing'
    ],
    long_description=long_description
)
