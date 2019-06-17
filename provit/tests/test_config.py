import yaml

from ..config import _load_provit_dir, Config, get_config


def test_load_provit_dir(tmp_path):
    custom_path = _load_provit_dir(tmp_path)
    assert tmp_path == custom_path
    assert custom_path.joinpath("config.yaml").is_file()


def test_load_provit_dir_from_config(tmp_path):
    orig_path = tmp_path / "orig"
    custom_path = tmp_path / "custom"
    for p in (orig_path, custom_path):
        p.mkdir()
    with open(orig_path / "config.yaml", "w") as config_file:
        config_file.write(yaml.dump({"provit_dir": str(custom_path.resolve())}))
    provit_dir = _load_provit_dir(orig_path)
    assert custom_path == provit_dir


def test_get_config(tmp_path):
    assert isinstance(get_config(), Config)
    c = get_config(tmp_path)
    assert isinstance(c, Config)
    assert c.provit_dir == tmp_path
    assert c.agents_dir == tmp_path / "agents"
    assert c.directories_file == tmp_path / "directories.yaml"
    c.agents_dir.joinpath("pytest-agent.yaml").touch()
    assert c.get_agent_profile("pytest-agent") is not None
    assert c.agent_profile_exists("pytest-agent-nonexistent") == False
