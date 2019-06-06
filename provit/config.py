"""
provit configuration

- Reads config.yaml from $HOME/.provit (or created new file if it doesn't exists)
- Sets up provit home directory with agents/activities directories and directories.yaml (if they don't exist)
- Provides CONFIG class, containing provit configuration information
"""


import os
import yaml
from pathlib import Path

def _add_dir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath

def _add_file(filepath):
    if not os.path.exists(filepath):
        open(filepath, "w")
    return filepath

def _load_provit_dir():
    os_home = str(Path.home())    
    provit_config_dir = _add_dir(os.path.join(os_home, ".provit"))
    filepath = _add_file(os.path.join(provit_config_dir, "config.yaml"))

    config = yaml.safe_load(open(filepath, "r"))

    if config:  
        if "provit_dir" in config:
            _add_dir(config["provit_dir"])
            return config["provit_dir"]

    return provit_config_dir
    

class CONFIG(object):

    PROVIT_DIR = _load_provit_dir()

    AGENTS_DIR = _add_dir(os.path.join(PROVIT_DIR, "agents"))

    DIRECTORIES_FILE = _add_file(os.path.join(PROVIT_DIR, "directories.yaml"))

    PERSON = 'Person'
    SOFTWARE = 'SoftwareAgent'
    ORGANIZATION = 'Organization'

    BASE_URI = "http://vocab.ub.uni-leipzig.de/provit/{}"

    @staticmethod
    def agent_profile_exists(slug):
        filepath = os.path.join(CONFIG.AGENTS_DIR, "{}.yaml".format(slug))
        return os.path.exists(filepath)


