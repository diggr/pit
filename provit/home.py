"""
Helper functions for accessing data in the provit home directory
"""

import os
import yaml

from .config import get_config
from .prov import load_prov_files
from .agent import agent_factory

cfg = get_config()


def load_directories(directories_file=None):
    """
    load the list of directories from the directories yaml file
    """

    if not directories_file:
        directories_file = cfg.directories_file
    with open(directories_file) as d_file:
        data = yaml.safe_load(d_file)

    if not data:
        data = {}

    if not isinstance(data, dict):
        raise IOError("invalid directories.yaml")

    for directory in data:
        if not os.path.exists(directory):
            data[directory]["exists"] = False
        else:
            data[directory]["exists"] = True

    rv = []
    for directory, content in data.items():
        rv.append(
            {
                "directory": directory,
                "comment": content["comment"],
                "exists": content["exists"],
            }
        )

    return rv


def remove_directories(directory):
    """
    Remove directories from project directory list
    """
    dirs = load_directories()
    dirs = [d for d in dirs if d["directory"] != directory["directory"]]
    _save_directories(dirs)

    return dirs


def add_directory(directory, directories_file=None):
    """
    Add directory to project directories list
    """
    dirs = load_directories(directories_file)

    # if directory already in current list do not add and return current list
    for d in dirs:
        if d["directory"] == directory["directory"]:
            return dirs

    dirs.append(directory)
    _save_directories(dirs, directories_file)
    return dirs


def _save_directories(directories, directories_file=None):
    """
    save current state of porject directories list to yaml file
    """
    data = {x["directory"]: {"comment": x["comment"].strip()} for x in directories}
    if not directories_file:
        directories_file = cfg.directories_file
    with open(directories_file, "w") as d_file:
        yaml.dump(data, d_file, default_flow_style=False)
