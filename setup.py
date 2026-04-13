#!/usr/bin/env python3
import os
from setuptools import setup, find_packages
from pathlib import Path
import platform

with open("README.md", encoding='utf8') as readme:
    long_description = readme.read()

setup(
    name="cfpsec",
    version="2.0.1",
    author="Alexandre Borges",
    author_email="reverseexploit@proton.me",
    license="GPL-3.0-or-later",
    url="https://github.com/alexandreborges/cfpsec",
    description=("CFPsec is a client program that retrieves the list of Call For Papers or/and upcoming Hacking/Security Conferences based on cfptime.org website."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    ],
    install_requires=[
        "colorama>=0.4.6",
        "requests>=2.26.0",
    ],
    entry_points={
        'console_scripts': [
            'cfpsec=cfpsec.cfpsec:main',
        ],
    },
    package_data={'': ['README.md, LICENSE']},
)
