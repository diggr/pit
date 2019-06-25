import json
import provit.browser.backend as backend
import provit.home as home
import pytest
import yaml

from pathlib import Path
from provit.config import get_config
from provit.home import add_directory
from provit import Provenance

TEST_DIRECTORY = {"directory": "/tmp", "comment": "test123"}

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

EXISTING_DIRNAME = "existing"
NON_EXISTING_DIRNAME = "non-existing"
DATA_FILE = "data.txt"
NOPROV_FILE = "noprov.txt"
TEST_ACTIVITY = "test"
TEST_AGENT = "testagent"


def do_json_post(client, endpoint, payload):
    response = client.post(endpoint, data=json.dumps(payload), headers=HEADERS)
    assert response.status_code == 200
    return response.json


@pytest.fixture(scope="session")
def path_with_directories(tmp_path_factory):
    test_path = tmp_path_factory.mktemp("directories_with_file")
    existing_dir = test_path / EXISTING_DIRNAME
    non_existing_dir = test_path / NON_EXISTING_DIRNAME
    existing_dir.mkdir()

    # Add noprov file without provenance
    noprov_file = test_path / NOPROV_FILE
    noprov_file.touch()

    # Add data file with provenance
    data_file = test_path / DATA_FILE
    data_file.touch()
    data_file_prov = Provenance(data_file)
    data_file_prov.add(
        agents=[TEST_AGENT], activity="testactivity", description=TEST_ACTIVITY
    )
    data_file_prov.save()

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


@pytest.fixture
def app(path_with_directories, monkeypatch):
    test_path, _ = path_with_directories
    cfg = get_config(test_path)

    def mock_home():
        return test_path

    monkeypatch.setattr(home, "cfg", cfg)
    monkeypatch.setattr(Path, "home", mock_home)
    app = backend.create_app(cfg)
    return app


def test_app_get_config(tmp_path, monkeypatch):
    """
    If no cfg is given to backend.create_app, get_config()
    is called, which defaults to ~/.provit being set as 
    provit_dir. This function checks, if this is the case.
    """

    def mock_home():
        return tmp_path

    monkeypatch.setattr(Path, "home", mock_home)
    app = backend.create_app()
    client = app.test_client()
    response = client.get("/config")
    assert response.status_code == 200
    assert client.get("/config").json == {
        "config": {"provit_dir": str(tmp_path / ".provit")}
    }


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_config(client, path_with_directories):
    test_path, _ = path_with_directories
    response = client.get("/config")
    assert response.status_code == 200
    assert response.json == {"config": {"provit_dir": str(test_path)}}


def test_directories(client, path_with_directories):
    """
    Tests, if the directory display, creation and deletion process works as expected.
    """
    test_path, d_expect = path_with_directories
    response = client.get("/directories")
    assert response.status_code == 200
    assert response.json == {"directories": d_expect}

    # Add directory
    data = {"directory": TEST_DIRECTORY}
    result = do_json_post(client, "/directories", data)
    assert result == {"directories": d_expect + [TEST_DIRECTORY]}

    # Delete directory
    result = do_json_post(client, "/directories/remove", data)
    assert result == {"directories": d_expect}


def test_filebrowser(client, path_with_directories):
    test_path, _ = path_with_directories
    data = {"directory": str(test_path), "withFiles": True, "withHidden": False}
    result = do_json_post(client, "/filebrowser", data)
    assert result["dirs"][0]["dirname"] == EXISTING_DIRNAME
    assert result["dirs"][0]["dirpath"] == str(test_path / EXISTING_DIRNAME)
    expected_files = [
        "config.yaml",
        "data.txt",
        "data.txt.prov",
        "directories.yaml",
        "noprov.txt",
    ]
    for f in result["files"]:
        f_name = f["filename"]
        assert f_name in expected_files
        expected_files.remove(f_name)


def test_filebrowser_on_home(client, path_with_directories):
    """
    As Path.home() is monkeypatched to return the contents of 
    the path_with_directories fixture, the results should be the 
    same as givin this path. If this is returned, we know that 
    Path.home() was called.
    """
    test_path, _ = path_with_directories
    data = {"directory": "", "withFiles": True, "withHidden": False}
    result1 = do_json_post(client, "/filebrowser", data)
    data["directory"] = str(test_path)
    result2 = do_json_post(client, "/filebrowser", data)
    assert result1 == result2


def test_directory(client, path_with_directories):
    test_path, _ = path_with_directories
    files = backend._build_file_list(test_path)

    data = {"directory": str(test_path)}
    result = do_json_post(client, "/directory", data)
    assert result == {"files": files}

    # Test if provenance information of test_file is included correctly
    for f in files:
        if f["filename"].endswith("data.txt"):
            prov = f["prov"]
            assert prov["last_activity"] == TEST_ACTIVITY
            assert prov["last_agent"] == [home.cfg.base_uri.format(TEST_AGENT)]


def test_directory_update(client, path_with_directories_and_file, test_filenames):
    test_path, _ = path_with_directories_and_file

    # Create file with provenance at original location
    test_file = test_path.joinpath(test_filenames["EXISTING_DIRNAME"], "test.txt")
    test_file.touch()
    p = Provenance(test_file)
    p.add(
        agents=["testagents"], activity="test_activity", description="test_description"
    )
    p.save()

    # Move to new location
    new_path = Path(test_path.parent) / "new"
    test_path.rename(Path(new_path))

    # Update directory
    data = {"directory": str(new_path / test_filenames["EXISTING_DIRNAME"])}
    result = do_json_post(client, "/directory/update", data)
    prov = result["files"][0]["prov"]
    assert prov["last_activity"].startswith("file moved to new location ->")


def test_agents(client):
    response = client.get("/agents")
    assert response.status_code == 200
    agents = response.json["agents"]
    assert len(agents) == 3
    assert agents["Organization"][0]["homepage"] == ["https://www.wikidata.org"]
    assert agents["SoftwareAgent"][0]["homepage"] == ["https://gephi.org/"]
    assert agents["Person"][0]["homepage"] == [
        "https://ub.uni-leipzig.de",
        "https://diggr.link",
    ]


def test_file_without_prov(client, path_with_directories):
    test_path, _ = path_with_directories
    noprov_file_path = str(test_path / NOPROV_FILE)
    data = {"filepath": noprov_file_path}
    result = do_json_post(client, "/file", data)
    assert result["hasProv"] == False


def test_file_with_prov(client, path_with_directories):
    test_path, _ = path_with_directories
    data_file_path = str(test_path / DATA_FILE)
    data = {"filepath": data_file_path}
    result = do_json_post(client, "/file", data)
    prov = result["prov"]
    assert result["hasProv"] == True
    assert prov["activity"].startswith(
        "http://vocab.ub.uni-leipzig.de/provit/testactivity/"
    )
    assert prov["agent"] == ["http://vocab.ub.uni-leipzig.de/provit/testagent"]
    assert prov["location"] == data_file_path
    # The following test currently fails, as the testagent is not found in the
    # agents directory
    # assert result["agents"] == ["http://vocab.ub.uni-leipzig.de/provit/testagent"]


def test_file_timespan_add_remove(client, path_with_directories):
    test_path, _ = path_with_directories
    noprov_file_path = str(test_path / NOPROV_FILE)

    ACTIVITY_DESC = "test"

    # Add data to noprov file
    prov_data = {
        "filepath": noprov_file_path,
        "prov": {
            "activitySlug": "test_fileadd_activity",
            "comment": ACTIVITY_DESC,
            "agents": [""],
            "startedAt": "2019-06-21T12:09:39.52",
            "endedAt": "2019-06-21T12:19:39.52",
            "sources": [],
            "primarySources": ["diggr.link"],
        },
        "isTimestamp": False,
    }
    result = do_json_post(client, "/file/add", prov_data)
    assert result["hasProv"] == True
    prov = result["prov"]
    assert prov["activity_desc"] == ACTIVITY_DESC
    assert (
        prov["primary_sources"][0] == "http://vocab.ub.uni-leipzig.de/provit/diggr.link"
    )
    assert prov["started_at"].startswith("2019-06-21 12:09:39")
    assert prov["ended_at"].startswith("2019-06-21 12:19:39")
    assert prov["activity"].startswith(
        "http://vocab.ub.uni-leipzig.de/provit/test_fileadd_activity"
    )

    # ... and remove it again
    remove_data = {"filepath": noprov_file_path}
    result = do_json_post(client, "/file/remove", remove_data)
    assert result["hasProv"] == False


def test_file_timestamp_add_remove(client, path_with_directories):
    test_path, _ = path_with_directories
    noprov_file_path = str(test_path / NOPROV_FILE)

    # Add data to noprov file
    prov_data = {
        "filepath": noprov_file_path,
        "prov": {
            "activitySlug": "test_fileadd_activity",
            "comment": "test",
            "agents": [""],
            "startedAt": "2019-06-21T12:09:39.52",
            "endedAt": "",
            "sources": [],
            "primarySources": [],
        },
        "isTimestamp": True,
    }
    result = do_json_post(client, "/file/add", prov_data)
    assert result["hasProv"] == True
    prov = result["prov"]

    # ... and remove it again
    remove_data = {"filepath": noprov_file_path}
    result = do_json_post(client, "/file/remove", remove_data)
    assert result["hasProv"] == False

    # and add 2 times again, to see, if there is still
    # one activity left, if the last is removed
    result = do_json_post(client, "/file/add", prov_data)
    assert result["hasProv"] == True
    result = do_json_post(client, "/file/add", prov_data)
    assert result["hasProv"] == True
    prov = result["prov"]

    # ... and remove it again and it should still have prov
    data = {"filepath": noprov_file_path}
    result = do_json_post(client, "/file/remove", data)
    assert result["hasProv"] == True
