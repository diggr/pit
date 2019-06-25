import provit.home as home
import pytest
import shutil
import yaml

from pathlib import Path
from provit.config import get_config

EXISTING_DIRNAME = "existing"
NON_EXISTING_DIRNAME = "non-existing"

TEST_FILE = "test.csv"
SOURCE_FILE = "source.csv"
INVALID_FILE = "invalid.csv"
NO_FILE = "no_file.csv"


@pytest.fixture(scope="session")
def test_filenames():
    return {
        "TEST_FILE": "test.csv",
        "SOURCE_FILE": "source.csv",
        "INVALID_FILE": "invalid.csv",
        "NO_FILE": "no_file.csv",
        "EXISTING_DIRNAME": "existing",
        "NON_EXISTING_DIRNAME": "non-existing",
    }


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


@pytest.fixture
def prov_path_with_agents(tmp_path_factory):
    prov_path = tmp_path_factory.mktemp("with_agents")
    cfg = get_config(prov_path)
    for agent_file in [
        "wikidata.yaml",
        "johndoe.yaml",
        "gephi_0.9.2.yaml",
        "invalid.yaml",
    ]:
        origin_path = Path(__file__).resolve().parent / "fixtures"
        shutil.copy(str(origin_path / agent_file), str(cfg.agents_dir))
    return prov_path


@pytest.fixture
def path_with_directories_and_file(tmp_path_factory):
    test_path = tmp_path_factory.mktemp("directories_with_file")
    existing_dir = test_path / EXISTING_DIRNAME
    non_existing_dir = test_path / NON_EXISTING_DIRNAME
    existing_dir.mkdir()

    d_content = {
        str(existing_dir.resolve()): {"comment": "test123"},
        str(non_existing_dir.resolve()): {"comment": "bla"},
    }
    d_expect = [
        {
            "directory": str(existing_dir.resolve()),
            "comment": "test123",
            "exists": True,
        },
        {
            "directory": str(non_existing_dir.resolve()),
            "comment": "bla",
            "exists": False,
        },
    ]
    home.cfg = get_config(test_path)
    with open(home.cfg.directories_file, "w") as dfile:
        yaml.dump(d_content, dfile)
    return test_path, d_expect
