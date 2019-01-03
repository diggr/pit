"""
provit configuration

- Reads config.yaml from $HOME/.provit (or created new file if it doesn't exists)
- Sets up provit home directory with agents/activities directories and directories.yaml (if they don't exist)
- Provides CONFIG class, containing provit configuration information
"""


import os
import yaml
from pathlib import Path

def add_dir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath

def add_file(filepath):
    if not os.path.exists(filepath):
        open(filepath, "w")
    return filepath

def load_provit_dir():
    os_home = str(Path.home())    
    provit_config_dir = add_dir(os.path.join(os_home, ".provit"))
    filepath = add_file(os.path.join(provit_config_dir, "config.yaml"))

    stream = open(filepath, "r")
    config = yaml.load(stream)

    if config:  
        if "provit_dir" in config:
            if not os.path.exists(config["provit_dir"]):
                os.makedirs(config["provit_dir"])
            return config["provit_dir"]

    return provit_config_dir
    

class CONFIG(object):

    PROVIT_DIR = load_provit_dir()
    AGENTS_DIR = add_dir(os.path.join(PROVIT_DIR, "agents"))
    ACTIVITIES_DIR = add_dir(os.path.join(PROVIT_DIR, "activities"))

    DIRECTORIES_FILE = add_file(os.path.join(PROVIT_DIR, "directories.yaml"))

    PERSON = 'Person'
    SOFTWARE = 'Software'
    ORGANIZATION = 'Organization'

    BASE_URI = "http://provit.diggr.link/{}"

    @staticmethod
    def agent_profile_exists(slug):
        filepath = os.path.join(CONFIG.AGENTS_DIR, "{}.yaml".format(slug))
        return os.path.exists(filepath)


