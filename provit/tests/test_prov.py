#!/usr/bin/env python
# coding: utf-8

"""
Tests for the proveneance object
"""
import json
import pytest
import shutil
import provit.prov

from provit.config import get_config
from pathlib import Path
from .. import Provenance


def test_load_prov_on_non_existing_file(tmp_path, test_filenames):
    assert provit.prov.load_prov(tmp_path / test_filenames["INVALID_FILE"]) == None


def test_load_prov_files(prov_files, test_filenames):
    assert provit.prov.load_prov_files(prov_files) == []
    prov = Provenance(prov_files / test_filenames["TEST_FILE"])
    prov.add(agents=["yada"], activity="testing", description="this is a testfunction")
    prov.save()
    loaded_prov = provit.prov.load_prov_files(prov_files)[0]
    assert loaded_prov.file_name == prov.file_name


def test_overwrite(prov_files, test_filenames):
    prov1 = Provenance(prov_files / test_filenames["TEST_FILE"])
    prov1.add(agents=["yada"], activity="testing", description="this is a testfunction")
    prov1.save()
    prov2 = Provenance(prov_files / test_filenames["TEST_FILE"], overwrite=True)
    prov2.add(
        agents=["yolo"], activity="test123", description="this is another testfunction"
    )
    prov2.save()
    assert prov2.tree()["agent"] == ["http://vocab.ub.uni-leipzig.de/provit/yolo"]


def test_incorrect_filepath(tmp_path, test_filenames):
    """
    Test if incorrect file name raises correct error
    """
    with pytest.raises(IOError):
        prov = Provenance(tmp_path / test_filenames["NO_FILE"])


def test_file_without_prov(prov_files, test_filenames):
    """
    Test if file with no prov information creates empty Provenance
    Object
    """
    prov = Provenance(prov_files / test_filenames["TEST_FILE"])
    assert prov.tree() == {}


def test_invalid_prov_file(invalid_prov_file):
    """
    Test if corrupt prov file raises correct error
    """
    with pytest.raises(json.decoder.JSONDecodeError):
        prov = Provenance(invalid_prov_file)


def test_add_incorrect_source_file(prov_files, test_filenames):
    """
    Test adding a incorrect file as source
    """

    prov = Provenance(prov_files / test_filenames["TEST_FILE"])
    prov.add(agents=["yada"], activity="testing", description="this is a testfunction")
    with pytest.raises(IOError):
        prov.add_sources([prov_files / test_filenames["NO_FILE"]])


def test_add_source_prov(prov_files, test_filenames):
    """
    Test if created prov information for prov source file (with no
    prior prov file) is correct
    """

    prov = Provenance(prov_files / test_filenames["TEST_FILE"])
    prov.add(agents=["yada"], activity="testing", description="this is a testfunction")
    prov.add_sources([prov_files / test_filenames["SOURCE_FILE"]])
    prov.save()

    assert len(prov.tree()["sources"]) == 1
    assert (
        prov.tree()["sources"][0]["agent"][0]
        == "http://vocab.ub.uni-leipzig.de/provit/provit"
    )
    assert "initialize_provit" in prov.tree()["sources"][0]["activity"]


def test_add_same_source_prov(prov_files, test_filenames):
    prov = Provenance(prov_files / test_filenames["TEST_FILE"])
    prov.add(agents=["yada"], activity="testing", description="this is a testfunction")
    prov.add_sources([prov_files / test_filenames["TEST_FILE"]])
    assert prov.tree()["sources"] == []


def test_get_agents(prov_files, test_filenames, prov_path_with_agents):
    provit.prov.cfg = get_config(prov_path_with_agents)
    prov = provit.prov.Provenance(prov_files / test_filenames["TEST_FILE"])
    prov.add(
        agents=["wikidata"], activity="testing", description="this is a testfunction"
    )
    prov.add(
        agents=["gephi_0.9.2"], activity="testing", description="this is a testfunction"
    )
    prov.add(
        agents=["johndoe"], activity="testing", description="this is a testfunction"
    )
    agent_list = prov.get_agents()
    assert len(agent_list) == 3
    assert prov.get_agents(include_primary_sources=True)["wikidata"] == {
        "slug": "wikidata",
        "uri": "http://vocab.ub.uni-leipzig.de/provit/wikidata",
        "type": "Organization",
        "name": ["Wikidata"],
        "homepage": ["https://www.wikidata.org"],
    }


def test_get_current_location(prov_files, test_filenames, prov_path_with_agents):
    provit.prov.cfg = get_config(prov_path_with_agents)
    prov = provit.prov.Provenance(prov_files / test_filenames["TEST_FILE"])
    prov.add(
        agents=["wikidata"], activity="testing", description="this is a testfunction"
    )
    assert str(prov.get_current_location()) == str(
        prov_files / test_filenames["TEST_FILE"]
    )


def test_empty_prov(prov_files, test_filenames):
    prov = provit.prov.Provenance(prov_files / test_filenames["TEST_FILE"])
    assert prov.tree() == {}
