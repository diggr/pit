import rdflib
import pytest
import shutil

import provit.agent as agent

from pathlib import Path
from provit.config import get_config

SA = {
    "name": ["Gephi"],
    "homepage": ["https://gephi.org/"],
    "slug": "gephi_0.9.2",
    "version": ["0.9.2"],
}
PA = {
    "name": ["John Doe", "J. Doe", "John Dö"],
    "homepage": ["https://ub.uni-leipzig.de", "https://diggr.link"],
    "email": ["john.doe@uni-leipzig.de", "doe.john@ub.uni-leipzig.de"],
    "institution": ["ubleipzig"],
    "slug": "johndoe",
}
OA = {}


@pytest.fixture
def prov_path_with_agents(tmp_path_factory):
    prov_path = tmp_path_factory.mktemp("with_agents")
    cfg = get_config(prov_path)
    for agent_file in [
        "wikidata.yaml",
        "johndoe.yaml",
        "gephi_0.9.2.yaml",
        "invalid.yaml",
    ]:
        origin_path = Path(__file__).resolve().parent / "fixtures"
        shutil.copy(str(origin_path / agent_file), str(cfg.agents_dir))
    return prov_path


def test_load_agent_profiles_on_empty(tmp_path):
    agent.cfg = get_config(tmp_path)
    agents = agent.load_agent_profiles()
    print(agents)
    assert agents == []


def test_load_agent_profile_invalid_agent(prov_path_with_agents):
    agent.cfg = get_config(prov_path_with_agents)
    assert agent.load_agent_profile("invalid") == None


def check_attrs(obj, reference):
    for key, value in reference.items():
        assert getattr(obj, key) == value


def test_load_agent_profiles(prov_path_with_agents):
    agent.cfg = get_config(prov_path_with_agents)
    agents = agent.load_agent_profiles()
    # First we check for correct structure of returned agents_list
    assert len(agents) == 3
    assert isinstance(agents[0], agent.SoftwareAgent)
    assert isinstance(agents[1], agent.PersonAgent)
    assert isinstance(agents[2], agent.OrganizationAgent)
    # Then we check for correct properties of each agent
    for i, a in enumerate([SA, PA, OA]):
        check_attrs(agents[i], a)


def test_agent_factory_on_empty():
    assert isinstance(agent.agent_factory("bla", agent.cfg.person), agent.PersonAgent)
    assert isinstance(
        agent.agent_factory("bla", agent.cfg.software), agent.SoftwareAgent
    )
    assert isinstance(
        agent.agent_factory("bla", agent.cfg.organization), agent.OrganizationAgent
    )


def test_agent_factory(prov_path_with_agents):
    agent.cfg = get_config(prov_path_with_agents)
    agents = agent.load_agent_profiles()
    check_attrs(agent.agent_factory("johndoe", agent.PersonAgent), PA)


def test_software_agent():
    assert agent.SoftwareAgent("test", uri="testuri").uri == "testuri"
    s_agent = agent.agent_factory("bla", agent.cfg.software)
    data = {
        "name": ["testagent"],
        "homepage": ["https://diggr.link"],
        "version": ["1.0"],
    }
    s_agent.update(data)
    assert s_agent.name == data["name"]
    assert s_agent.homepage == data["homepage"]
    assert s_agent.version == data["version"]
    for key in ["uri", "type", "slug", "name", "version", "homepage"]:
        assert key in s_agent.to_json()
    for key, value in data.items():
        assert s_agent.to_json()[key] == value
    assert isinstance(s_agent.graph(), rdflib.graph.Graph)


def test_organization_agent():
    assert agent.OrganizationAgent("bla", uri="testuri").uri == "testuri"
    data = {"name": ["testorganization"], "homepage": ["https://diggr.link"]}
    o_agent = agent.agent_factory("bla", agent.cfg.organization)
    o_agent.update(data)
    assert o_agent.name == data["name"]
    assert o_agent.homepage == data["homepage"]
    for key in ["uri", "type", "slug", "name", "homepage"]:
        assert key in o_agent.to_json()
    assert isinstance(o_agent.graph(), rdflib.graph.Graph)


def test_person_agent():
    assert agent.PersonAgent("bla", uri="testuri").uri == "testuri"
    data = {
        "name": ["testperson"],
        "homepage": ["https://diggr.link"],
        "email": ["test"],
        "institution": ["ubleipzig"],
    }
    p_agent = agent.agent_factory("bla", agent.cfg.person)
    p_agent.update(data)
    assert p_agent.name == data["name"]
    assert p_agent.homepage == data["homepage"]
    assert p_agent.institution == data["institution"]
    assert p_agent.email == data["email"]
    for key in ["uri", "type", "slug", "name", "homepage", "email", "institution"]:
        assert key in p_agent.to_json()
    assert isinstance(p_agent.graph(), rdflib.graph.Graph)
