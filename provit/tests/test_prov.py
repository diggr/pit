#!/usr/bin/env python
# coding: utf-8

"""
Tests for the proveneance object
"""
import json
import pytest
import shutil
import provit.prov

from pathlib import Path
from .. import Provenance


TEST_FILE = "test.csv"
SOURCE_FILE = "source.csv"
INVALID_FILE = "invalid.csv"
NO_FILE = "no_file.csv"


@pytest.fixture
def prov_files(tmp_path_factory):
    base_path = tmp_path_factory.mktemp("prov_files")
    for f in (TEST_FILE, SOURCE_FILE):
        base_path.joinpath(f).touch()
    return base_path


@pytest.fixture(scope="session")
def invalid_prov_file(tmp_path_factory):
    base_path = tmp_path_factory.getbasetemp()
    invalid_file = base_path.joinpath(INVALID_FILE)
    invalid_file.touch()
    with open(base_path / f"{INVALID_FILE}.prov", "w") as invalid:
        invalid.write("bla")
    return invalid_file


def test_load_prov_on_non_existing_file(tmp_path):
    assert provit.prov.load_prov(tmp_path / INVALID_FILE) == None


def test_load_prov_files(prov_files):
    assert provit.prov.load_prov_files(prov_files) == []
    prov = Provenance(prov_files / TEST_FILE)
    prov.add(agents=["yada"], activity="testing", description="this is a testfunction")
    prov.save()
    loaded_prov = provit.prov.load_prov_files(prov_files)[0]
    assert loaded_prov.file_name == prov.file_name


def test_overwrite(prov_files):
    prov1 = Provenance(prov_files / TEST_FILE)
    prov1.add(agents=["yada"], activity="testing", description="this is a testfunction")
    prov1.save()
    prov2 = Provenance(prov_files / TEST_FILE, overwrite=True)
    prov2.add(
        agents=["yolo"], activity="test123", description="this is another testfunction"
    )
    prov2.save()
    assert prov2.tree()["agent"] == ["http://vocab.ub.uni-leipzig.de/provit/yolo"]


def test_incorrect_filepath(tmp_path):
    """
    Test if incorrect file name raises correct error
    """
    with pytest.raises(IOError):
        prov = Provenance(tmp_path / NO_FILE)


def test_file_without_prov(prov_files):
    """
    Test if file with no prov information creates empty Provenance
    Object
    """
    prov = Provenance(prov_files / TEST_FILE)
    assert prov.tree() == {}


def test_invalid_prov_file(invalid_prov_file):
    """
    Test if corrupt prov file raises correct error
    """
    with pytest.raises(json.decoder.JSONDecodeError):
        prov = Provenance(invalid_prov_file)


def test_add_incorrect_source_file(prov_files):
    """
    Test adding a incorrect file as source
    """

    prov = Provenance(prov_files / TEST_FILE)
    prov.add(agents=["yada"], activity="testing", description="this is a testfunction")
    with pytest.raises(IOError):
        prov.add_sources([prov_files / NO_FILE])


def test_add_source_prov(prov_files):
    """
    Test if created prov information for prov source file (with no
    prior prov file) is correct
    """

    prov = Provenance(prov_files / TEST_FILE)
    prov.add(agents=["yada"], activity="testing", description="this is a testfunction")
    prov.add_sources([prov_files / SOURCE_FILE])
    prov.save()

    assert len(prov.tree()["sources"]) == 1
    assert (
        prov.tree()["sources"][0]["agent"][0]
        == "http://vocab.ub.uni-leipzig.de/provit/provit"
    )
    assert "initialize_provit" in prov.tree()["sources"][0]["activity"]
