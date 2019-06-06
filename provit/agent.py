"""
Everything agent profile related


1. Classes

* Person
* SoftwareAgent
* Organization

Each class contains :to_json(): and :graph(): functions,
returning the data of the classes either as json-dict or
rdflib Graph.


2. Helper functions

* load_agent_profile(slug) 
  loads the yaml file of agent :slug: and initiates the 
  respective agent class (depending on type)

* load_agent_profiles() 
  loads all agent yaml files and returns a list of 
  agent classes

* agent_factory(slug, type_) 
  initializes an agent class of type :type_: with id/uri
  :slug:

"""

import os
import yaml

from rdflib import Graph, Literal
from rdflib.namespace import FOAF, URIRef, Namespace, RDF

from .namespaces import PROVIT, PROV, SCHEMA
from .config import CONFIG as CF


def _get_element_or_alt(data, element, alt):
    """
    if :element: is in dict :data: return it, otherwise 
    return :alt:
    """
    if element in data:
        return data[element]
    else:
        return alt


def load_agent_profile(slug):
    """
    loads agent yaml profile (if available) and initiates agent 
    class with the values obtained from the yaml file
    """
    filepath = os.path.join(CF.AGENTS_DIR, "{}.yaml".format(slug))
    if not os.path.exists(filepath):
        return None
    
    data = yaml.safe_load(open(filepath, "r"))
    
    if data["type"] == CF.PERSON:
        uri = _get_element_or_alt(data, "uri", "")
        name = _get_element_or_alt(data, "name", [])
        institution = _get_element_or_alt(data, "institution", [])
        homepage = _get_element_or_alt(data, "homepage", [])
        email = _get_element_or_alt(data, "email", []) 

        return PersonAgent(
            slug=slug, 
            name=name,
            uri=uri,
            institution=institution,
            homepage=homepage,
            email=email
        )

    elif data["type"] == CF.ORGANIZATION:
        uri = _get_element_or_alt(data, "uri", "")
        name = _get_element_or_alt(data, "name", [])
        homepage = _get_element_or_alt(data, "homepage", [])

        return OrganizationAgent(
            slug=slug,
            name=name,
            uri=uri,
            homepage=homepage
        )

    elif data["type"] == CF.SOFTWARE:
        uri = _get_element_or_alt(data, "uri", "")
        name = _get_element_or_alt(data, "name", "")
        version = _get_element_or_alt(data, "version", "")
        homepage = _get_element_or_alt(data, "homepage", "")

        return SoftwareAgent(
            slug=slug,
            uri=uri,
            name=name,
            version=version,
            homepage=homepage
        )

    return None


def load_agent_profiles():
    agents = []
    for filename in os.listdir(CF.AGENTS_DIR):
        print(filename)
        filepath = os.path.join(CF.AGENTS_DIR, filename)
        slug = filename.replace(".yaml", "")

        agents.append(load_agent_profile(slug))

    return [x for x in agents if x ]


def agent_factory(slug, type_):
    """
    return "empty" agent class instance of the specified type
    """
    if CF.agent_profile_exists(slug):
        return load_agent_profile(slug)
    else:
        if type_ == CF.PERSON:
            return PersonAgent(slug)
        elif type_ == CF.SOFTWARE:
            return SoftwareAgent(slug)
        elif type_ == CF.ORGANIZATION:
            return OrganizationAgent(slug)


class OrganizationAgent(object):
    def __init__(self, slug, name=[], homepage=[], uri=""):
        self.type = CF.ORGANIZATION
        self.slug = slug
        if uri:
            self.uri = uri
        else:
            self.uri = PROVIT[slug]
        self.name = name
        self.homepage = homepage

    def update(self, data):
        self.name = list( set(self.name).union(set(data["name"])) )
        self.homepage = list( set(self.homepage).union(set(data["homepage"])) )

    def to_json(self):
        return {
            "uri": self.uri,
            "slug": self.slug,
            "type": self.type,
            "name": self.name,
            "homepage": self.homepage
        }

    def graph(self):
        uri = URIRef(self.uri)
        g = Graph()

        g.add( (uri, RDF.type, PROV.Organization) )

        for name in self.name:
            g.add( (uri, FOAF.name, Literal(name)) )
        for homepage in self.homepage:
            g.add( (uri, FOAF.homepage, Literal(homepage)) )

        return g


class PersonAgent(object):
    def __init__(self, slug, name=[], institution=[], homepage=[], email=[], uri=""):
        self.type = CF.PERSON
        self.slug = slug
        if uri:
            self.uri = uri
        else:
            self.uri = PROVIT[slug]
        self.name = name
        self.institution = institution
        self.homepage = homepage
        self.email = email

    def update(self, data):
        self.name = list( set(self.name).union(set(data["name"])) )
        self.homepage = list( set(self.homepage).union(set(data["homepage"])) )
        self.email = list( set(self.email).union(set(data["email"])) )
        self.institution = list( set(self.institution).union(set(data["institution"])) )

    def to_json(self):
        return {
            "uri": self.uri,
            "type": self.type,
            "slug": self.slug,
            "name": self.name,
            "institution": self.institution,
            "homepage": self.homepage,
            "email": self.email
        }

    def graph(self):
        uri = URIRef(self.uri)
        g = Graph()

        g.add( (uri, RDF.type, PROV.Person) )

        for name in self.name:
            g.add( (uri, FOAF.name, Literal(name)) )
        for institution in self.institution:
            g.add( (uri, FOAF.member, PROVIT[institution]) )
        for homepage in self.homepage:
            g.add( (uri, FOAF.homepage, Literal(homepage)) )
        for email in self.email:
            g.add( (uri, FOAF.mbox, Literal(email)) )

        return g


class SoftwareAgent(object):
    def __init__(self, slug, name=[], version=[], homepage=[], uri=""):
        self.type = CF.SOFTWARE
        self.slug = slug
        if uri:
            self.uri = uri
        else:
            self.uri = PROVIT[slug]
        self.name = name
        self.version = version
        self.homepage = homepage

    def update(self, data):
        self.name = list( set(self.name).union(set(data["name"])) )
        self.homepage = list( set(self.homepage).union(set(data["homepage"])) )
        self.version = list( set(self.version).union(set(data["version"])) )

    def to_json(self):
        return {
            "uri": self.uri,
            "type": self.type,
            "slug": self.slug,
            "name": self.name,
            "version": self.version,
            "homepage": self.homepage
        }
    
    def graph(self):
        uri = URIRef(self.uri)
        g = Graph()
        g.add( (uri, RDF.type, PROV.SoftwareAgent) )
        for name in self.name:
            g.add( (uri, FOAF.name, Literal(name)) )
        for version in self.version:
            g.add( (uri, SCHEMA.softwareVersion, Literal(version)) )
        for homepage in self.homepage:
            g.add( (uri, FOAF.homepage, Literal(homepage)) )
        return g
