#!/usr/bin/env python3
import os
from setuptools import setup, find_packages
from pathlib import Path
import platform

with open("README.md", encoding='utf8') as readme:
    long_description = readme.read()

setup(
    name="cfpsec",
    version="1.2",
    author="Alexandre Borges",
    author_email="alexandreborges@blackstormsecurity.com",
    license="GNU GPL v3.0",
    url="https://github.com/alexandreborges/cfpsec",
    description=("CFPsec is a client program that retrieves the list of Call For Papers or/and upcoming Hacking/Security Conferences based on cfptime.org website."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
    'Operating System :: OS Independent',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3',
    ],
    install_requires=[
        "colorama",
        "simplejson",
        "requests",
    ],
    scripts=['cfpsec/cfpsec.py'],
    package_data={'': ['README.md, LICENSE']},
)
