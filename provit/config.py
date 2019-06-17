"""
provit configuration module

provides the Config-class as well as its factory method get_config.

By default, $HOME/.provit is assumed to be provits default config directory.
This can be customized.
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
    person: str = "Person"
    software: str = "SoftwareAgent"
    organization: str = "Organization"
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

    def agent_profile(self, slug):
        return self.agents_dir.joinpath(f"{slug}.yaml")

    def agent_profile_exists(self, slug):
        return self.agent_profile(slug).is_file()

    def get_agent_profile(self, slug):
        if self.agent_profile_exists(slug):
            return self.agent_profile(slug)
        else:
            return None


def get_config(provit_dir=None):
    """
    factory method for Config class. can be given a custom provit dir.
    If no directory is given, the default directory ~/.provit will be
    chosen.
    """
    return Config(provit_dir=_load_provit_dir(provit_dir))
