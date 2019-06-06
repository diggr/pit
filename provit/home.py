"""
Helper functions for accessing data in the provit home directory
"""

import os
import yaml

from .config import CONFIG 
from .utils import combine_agents
from .prov import load_prov_files 
from .agent import agent_factory

def _iter_prov_files():
    """
    iterate through all prov files in all project directories
    """
    for directory in load_directories():
        for prov in load_prov_files(directory):
            yield prov


def generate_agent_profiles():
    """
    iterates through all prov files in the project directories and generates
    a yaml files for each agent in the prov files
    """
    agent_list = {}
    for prov in _iter_prov_files():
        new_agents = prov.get_agents(include_primary_sources=True)
        for slug, data in new_agents.items():
            if not slug in agent_list:
                profile = agent_factory(slug, data["type"])
                agent_list[slug] = profile
            agent_list[slug].update(data)
            
    for slug, profile in agent_list.items():
        filename = os.path.join(CONFIG.AGENTS_DIR, "{}.yaml".format(slug))
        with open(filename, "w") as f:
            yaml.dump(profile.to_json(), f, default_flow_style=False)        


def load_directories():
    """
    load the list of directories from the directories yaml file
    """
    stream = open(CONFIG.DIRECTORIES_FILE, "r")
    data = yaml.safe_load(stream)

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
        rv.append({
            "directory": directory,
            "comment": content["comment"],
            "exists": content["exists"]
        })

    return rv     
    

def remove_directories(directory):
    """
    Remove directories from project directory list
    """
    dirs = load_directories()
    dirs = [ d for d in dirs if d["directory"] !=  directory["directory"]]
    _save_directories(dirs)

    return dirs


def add_directory(directory):
    """
    Add directory to project directories list
    """
    dirs = load_directories()
    
    # if directory already in current list do not add and return current list
    for d in dirs:
        if d["directory"] == directory["directory"]:
            return dirs

    dirs.append(directory)
    _save_directories(dirs)
    return dirs


def _save_directories(directories):
    """
    save current state of porject directories list to yaml file
    """
    data = { x["directory"]: { "comment": x["comment"].strip() } for x in directories }
    yaml.dump(data, open(CONFIG.DIRECTORIES_FILE, "w"), default_flow_style=False)
