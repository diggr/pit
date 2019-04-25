#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import dirname, abspath, join

base_path = dirname(abspath(__file__))

with open(join(base_path, "README.rst")) as readme_file:
    readme = readme_file.read()

with open(join(base_path, "requirements.txt")) as req_file:
    requirements = req_file.readlines()

setup(
    name="provit",
    description='A light, dezentralized provenance tracking framework using the W3C PROV-O vocabulary',
    long_description=readme,
    license="MIT",
    author='Diggr Team',
    author_email='team@diggr.link',
    url='https://github.com/diggr/provit',
    packages=find_packages(exclude=['dev', 'docs']),
    package_dir={
            'provit': 'provit'
        },
    version="1.0.1",
    py_modules=["provit", "browser"],
    install_requires=requirements,
    include_package_data=True,
    entry_points="""
        [console_scripts]
        provit=provit.cli:cli
    """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: System :: Logging',
    ],
    keywords=[
        'provenance', 'cli', 'model', 'PROV', 'PROV-DM', 'PROV-JSON', 'JSON',
        'PROV-XML', 'PROV-N', 'PROV-O', 'RDF', "JSON-LD"
    ],
)
