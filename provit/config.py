"""
provit configuration

- Reads config.yaml from $HOME/.provit (or created new file if it doesn't exists)
- Sets up provit home directory with agents/activities directories and directories.yaml (if they don't exist)
- Provides CONFIG class, containing provit configuration information
"""


import yaml
import warnings
from pathlib import Path
from dataclasses import dataclass

DIRECTORIES_FILE = "directories.yaml"
CONFIG_FILE = "config.yaml"
AGENTS_DIR = "agents"
PROVIT_DIR = ".provit"

def _load_provit_dir(custom_provit_config_dir=None):
    if custom_provit_config_dir:
        provit_config_dir = Path(custom_provit_config_dir)
    else:
        provit_config_dir = Path.home().joinpath(PROVIT_DIR)

    provit_config_dir.mkdir(parents=True, exist_ok=True)
    config_path = provit_config_dir / CONFIG_FILE
    config_path.touch()

    with open(config_path) as config_file:
        config = yaml.safe_load(config_file)

    if config and "provit_dir" in config:
        return Path(config["provit_dir"])

    return provit_config_dir


@dataclass
class Config:
    provit_dir: Path
    person: str  = 'Person'
    software: str = 'SoftwareAgent'
    organization: str = 'Organization'
    base_uri: str = "http://vocab.ub.uni-leipzig.de/provit/{}"

    @property
    def agents_dir(self):
        a_dir = self.provit_dir / AGENTS_DIR
        a_dir.mkdir(exist_ok=True)
        return a_dir

    @property
    def directories_file(self):
        d_file = self.provit_dir / DIRECTORIES_FILE
        d_file.touch()
        return d_file

    def agent_profile_exists(self, slug):
        return self.agents_dir.joinpath(f"{slug}.yaml").is_file()

def get_config(provit_dir=None):
    """
    factory method for Config class. can be given a custom provit dir.
    If no directory is given, the default directory ~/.provit will be
    chosen.
    """
    return Config(provit_dir=_load_provit_dir(provit_dir))



class CONFIG(object):

    warnings.warn("The CONFIG class is deprecated and should not be used anymore. Use the Config class instead.", DeprecationWarning, stacklevel=2)

    PROVIT_DIR = _load_provit_dir()

    AGENTS_DIR = PROVIT_DIR.joinpath("agents")
    AGENTS_DIR.mkdir(exist_ok=True)

    DIRECTORIES_FILE = PROVIT_DIR / "directories.yaml"
    DIRECTORIES_FILE.touch()

    PERSON = 'Person'
    SOFTWARE = 'SoftwareAgent'
    ORGANIZATION = 'Organization'

    BASE_URI = "http://vocab.ub.uni-leipzig.de/provit/{}"

    @staticmethod
    def agent_profile_exists(slug):
        filepath = CONFIG.AGENTS_DIR / "{}.yaml".format(slug)
        return filepath.is_file()


