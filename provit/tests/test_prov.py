#!/usr/bin/env python
# coding: utf-8

"""
Tests for the proveneance object
"""

from .. import Provenance
import pytest
import shutil
import json
from pathlib import Path


def setup_module(module):
    Path('provit/tests/tmp/').mkdir()
    Path('provit/tests/tmp/test.csv').touch()
    Path('provit/tests/tmp/source.txt').touch()

    Path('provit/tests/tmp/invalid.csv').touch()
    with open('provit/tests/tmp/invalid.csv.prov', 'w') as invalid:
        invalid.write('bla')

def teardown_module(module):
    shutil.rmtree('provit/tests/tmp')


def test_incorrect_filepath():
    """
    Test if incorrect file name raises correct error
    """
    with pytest.raises(IOError):
        prov = Provenance('no_file.csv')

def test_file_without_prov():
    """
    Test if file with no prov information creates empty Provenance
    Object
    """
    prov = Provenance('provit/tests/tmp/test.csv')
    assert prov.tree() == {}

def test_invalid_prov_file():
    """
    Test if corrupt prov file raises correct error
    """    
    with pytest.raises(json.decoder.JSONDecodeError):
        prov = Provenance('provit/tests/tmp/invalid.csv')

