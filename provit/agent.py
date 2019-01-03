import os
import yaml

from rdflib import Graph, Literal
from rdflib.namespace import FOAF, URIRef, Namespace, RDF
from .namespaces import PROVIT, PROV

from .config import CONFIG as CF
from .utils import provit_uri


def get_element_or_empty(data, element, alt):
    if element in data:
        return data[element]
    else:
        return alt

def load_agent_profile(slug):
    filepath = os.path.join(CF.AGENTS_DIR, "{}.yaml".format(slug))
    if not os.path.exists(filepath):
        return None
    
    data = yaml.load(open(filepath, "r"))
    
    if data["type"] == CF.PERSON:
        uri = get_element_or_empty(data, "uri", "")
        name = get_element_or_empty(data, "name", [])
        institution = get_element_or_empty(data, "institution", [])
        homepage = get_element_or_empty(data, "homepage", [])
        email = get_element_or_empty(data, "email", []) 

        return PersonAgent(
            slug=slug, 
            name=name,
            uri=uri,
            institution=institution,
            homepage=homepage,
            email=email
        )

    elif data["type"] == CF.ORGANIZATION:
        uri = get_element_or_empty(data, "uri", "")
        name = get_element_or_empty(data, "name", [])
        homepage = get_element_or_empty(data, "homepage", [])

        return OrganizationAgent(
            slug=slug,
            name=name,
            uri=uri,
            homepage=homepage
        )

    elif data["type"] == CF.SOFTWARE:
        uri = get_element_or_empty(data, "uri", "")
        name = get_element_or_empty(data, "name", "")
        version = get_element_or_empty(data, "version", "")
        homepage = get_element_or_empty(data, "homepage", "")

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
        filepath = os.path.join(CF.AGENTS_DIR, filename)
        slug = filename.replace(".yaml", "")

        agents.append(load_agent_profile(slug))

    return [x for x in agents if x ]


def agent_factory(slug, type_):
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
            self.uri = provit_uri(slug)
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

        g.add( (uri, RDF.type, FOAF.Organization) )

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
            self.uri = provit_uri(slug)
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

        g.add( (uri, RDF.type, FOAF.Person) )

        for name in self.name:
            g.add( (uri, FOAF.name, Literal(name)) )
        for institution in self.institution:
            g.add( (uri, PROVIT.institution, Literal(institution)) )
        for homepage in self.homepage:
            g.add( (uri, FOAF.homepage, Literal(homepage)) )
        for email in self.email:
            g.add( (uri, PROVIT.email, Literal(email)) )

        return g

class SoftwareAgent(object):
    def __init__(self, slug, name=[], version=[], homepage=[], uri=""):
        self.type = CF.SOFTWARE
        self.slug = slug
        if uri:
            self.uri = uri
        else:
            self.uri = provit_uri(slug)
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
        g.add( (uri, RDF.type, PROVIT.Software) )
        for name in self.name:
            g.add( (uri, FOAF.name, Literal(name)) )
        for version in self.version:
            g.add( (uri, PROVIT.softwareVersion, Literal(version)) )
        for homepage in self.homepage:
            g.add( (uri, FOAF.homepage, Literal(homepage)) )
        return g