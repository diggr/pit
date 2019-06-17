import click
import pytest
import shutil

from click.testing import CliRunner
from pathlib import Path

from ..cli import cli
from ..prov import Provenance, load_prov

ADD_OPTIONS_LIST = (
    (["--agent", "testagent"], 1),
    (["--comment", "test"], 1),
    (["--activity", "testing"], 0),
    #    ["--origin", "diggr.link"],
)

TEST_FILE = {"file": "test_file.txt", "prov": "test_file.txt.prov"}


def add_test_prov(test_file):
    p = Provenance(test_file)
    p.add(
        agents=[ADD_OPTIONS_LIST[0][0][1]],
        activity=ADD_OPTIONS_LIST[2][0][1],
        description=ADD_OPTIONS_LIST[1][0][1],
    )
    p.save()


@pytest.fixture
def test_file_path(tmp_path_factory):
    base_path = tmp_path_factory.getbasetemp()
    test_file = base_path / TEST_FILE["file"]
    prov_file = base_path / TEST_FILE["prov"]
    test_file.touch()
    return test_file, prov_file


@pytest.fixture
def test_file_with_prov(tmp_path_factory):
    base_path = tmp_path_factory.getbasetemp()
    test_file = base_path / TEST_FILE["file"]
    prov_file = base_path / TEST_FILE["prov"]
    test_file.touch()
    add_test_prov(test_file)
    return base_path, test_file, prov_file


def test_browser_fail_on_invalid_dir(tmp_path):
    non_existing_path = tmp_path / "non_existing"
    runner = CliRunner()
    result = runner.invoke(cli, ["browser", str(non_existing_path)])
    assert result.exit_code == 1


def test_cli_with_invalid_dir(tmp_path):
    non_existing_path = tmp_path / "non_existing"
    runner = CliRunner()
    result = runner.invoke(cli, ["add", str(non_existing_path)])
    assert result.exit_code == 1
    assert result.output == "Invalid filepath\n"


def test_cli_agent_activity_comment(test_file_path):
    test_file, prov_file = test_file_path
    options = []
    for i in range(3):
        options += ADD_OPTIONS_LIST[i][0]
        runner = CliRunner()
        result = runner.invoke(cli, ["add"] + options + [str(test_file)])
        assert result.exit_code == ADD_OPTIONS_LIST[i][1]
    assert prov_file.is_file()
    p = load_prov(test_file)
    assert isinstance(p, Provenance)
    assert p.tree()["agent"] == [
        "http://vocab.ub.uni-leipzig.de/provit/{}".format(ADD_OPTIONS_LIST[0][0][1])
    ]
    assert p.tree()["activity"].startswith(
        "http://vocab.ub.uni-leipzig.de/provit/{}/".format(ADD_OPTIONS_LIST[2][0][1])
    )
    assert p.tree()["activity_desc"] == ADD_OPTIONS_LIST[1][0][1]


def test_cli_add_primary_source(test_file_with_prov):
    primary_source = "asdasd123456789"
    base_path, test_file, prov_file = test_file_with_prov
    runner = CliRunner()
    result = runner.invoke(cli, ["add", "--origin", primary_source, str(test_file)])
    assert result.exit_code == 0
    p = load_prov(test_file)
    assert isinstance(p, Provenance)
    assert (
        f"http://vocab.ub.uni-leipzig.de/provit/{primary_source}"
        in p.get_primary_sources()
    )


def test_cli_add_origin(test_file_with_prov):
    base_path, test_file, prov_file = test_file_with_prov
    new_file = base_path / "new.txt"
    new_file.touch()
    add_test_prov(new_file)
    runner = CliRunner()
    result = runner.invoke(cli, ["add", "--origin", str(test_file), str(new_file)])
    assert result.exit_code == 0
    p = Provenance(new_file)
    assert p.tree()["primary_sources"][0][
        "uri"
    ] == "http://vocab.ub.uni-leipzig.de/provit" + str(test_file)
