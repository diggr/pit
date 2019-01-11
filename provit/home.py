"""
Helper functions for accessing data in the provit home directory
"""

import os
import yaml

from .config import CONFIG 
from .utils import combine_agents
from .prov import load_prov_files 
from .agent import agent_factory 

def iter_prov_files():
    for directory in load_directories():
        for prov in load_prov_files(directory):
            yield prov


def generate_agent_profiles():
    agent_list = {}
    for prov in iter_prov_files():
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
    data = yaml.load(stream)
    print(data, CONFIG.DIRECTORIES_FILE)

    if not isinstance(data, dict):
        raise IOError("directories.yaml does not contain a list")

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

    print(rv)

    return rv     
    
def remove_directories(directory):
    dirs = load_directories()
    dirs.remove(directory)

    #save dirs

    return dirs

def add_directory(directory):
    dirs = load_directories()
    dirs.append(directory)

    #save dirs

    return dirs


def load_agents():
    pass

def load_activities():
    pass