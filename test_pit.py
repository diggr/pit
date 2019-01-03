#!/usr/bin/env python3
"""
This file contains the software tests.
"""

from click.testing import CliRunner

from provit.home import load_directories
from provit.config import CONFIG as C
from provit.agent import load_agent_profiles
from provit.browser.backend import start_browser
from provit.prov import Provenance
from provit.agent import load_agent_profiles
from provit.home import generate_agent_profiles

def setup_module():
    global runner
    runner = CliRunner()


def test_empty_argument():
    result = runner.invoke(cli)
    assert result.exit_code == 2


def test_path_as_argument():
    result = runner.invoke(cli, ["."])
    assert result.exit_code == 1

def test():
    init()

if __name__  == "__main__":

    print(load_directories())
    #start_browser()
    agents = load_agent_profiles()
    #for agent in agents:
    #    print(agent.graph())
    #prov = Provenance("/home/pmuehleder/test/analysis.gephi")
    #print(prov.get_agents())
    generate_agent_profiles()