import provit.home as home
import pytest
import yaml

from pathlib import Path
from jinja2 import Template
from ..config import get_config


def test_load_directories_no_file(tmp_path):
    home.cfg = get_config(tmp_path)
    assert len(home.load_directories()) == 0


def test_load_directories_invalid_file(tmp_path):
    home.cfg = get_config(tmp_path)
    with open(home.cfg.directories_file, "w") as dfile:
        yaml.dump([1, 2, 3], dfile)
    with pytest.raises(IOError):
        home.load_directories()


def test_load_directories_read_directories(path_with_directories_and_file):
    test_path, directories_expect = path_with_directories_and_file
    home.cfg = get_config(test_path)
    assert home.load_directories() == directories_expect


def test_add_and_remove_directories(path_with_directories_and_file):
    test_path, directories_expect = path_with_directories_and_file
    home.cfg = get_config(test_path)
    assert home.remove_directories(directories_expect[1]) == directories_expect[:-1]
    # Do it again, to see if nothing changed
    assert home.remove_directories(directories_expect[1]) == directories_expect[:-1]
    assert home.add_directory(directories_expect[1]) == directories_expect
    # Do it again, to see if nothing changed
    assert home.add_directory(directories_expect[1]) == directories_expect
