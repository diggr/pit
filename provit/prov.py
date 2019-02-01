"""
Provenance class handles provenance metadata information.

Use:

from pit.prov import Provenance

#load prov data for a file, or create new prov for file
prov = Provenance(<filepath>)

#add provenance metadata
prov.add(agent="agent", activity="activity", description="...")
prov.add_primary_source("primary_source", url="http://...", comment="...")
prov.add_sources(["filepath1", "filepath2"])

#return provenance as json tree
prov_dict = prov.tree()

#save provenance metadata into "<filename>.prov" file
prov.save()
"""

import uuid
import os

from datetime import datetime
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, FOAF, RDFS

from .namespaces import PROV, PROVIT, SCHEMA
from .utils import load_jsonld
from .config import CONFIG as CF
from .agent import load_agent_profile


def load_prov(filepath, namespace=PROVIT):
    """
    Loads a Provenance Object from the given file path or returns None if no (valid) provenance file was found.
    :param filepath:
    :return:
    """
    prov_filepath = "{}.prov".format(filepath)
    if os.path.exists(prov_filepath):
        return Provenance(filepath, namespace=namespace)
    else:
        return None


def load_prov_files(directory):
    files = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if not filename.endswith(".prov") and not os.path.isdir(filepath):
            
            prov = None
            prov_file = "{}.prov".format(filepath)
            if os.path.exists(prov_file):
                print(prov_file)
                prov_data = Provenance(filepath)
                files.append(prov_data)
            
    return files

class Provenance(object):
    """
    Provenance class handles the provenance metadata graph
    """

    def __init__(self, filepath, namespace=None, create_new=True, overwrite=False):
        """
        Initialize object with provenance graph for file :filepath:
        If no provenance file is available create new provenance graph
        """
        self.graph = Graph()
        self.file_name = os.path.basename(filepath)

        self.prov_filepath = "{}.prov".format(filepath)
        self.location = os.path.abspath(filepath)
        self.timestamp = datetime.now().isoformat()

        self.namespace = namespace

        if overwrite:
            self._set_up_context(namespace=namespace)
            self.init = True
            self.entity = self._generate_entity_node()

        else:            
            g, context = load_jsonld(self.prov_filepath)
            if g and context:
                self.init = False
                self.context = context
                self.graph = g
                self.entity = self._get_root_entity()
                if "provit" not in context:
                    self.context["provit"] = PROVIT
                self.namespace = self.context["provit"]
            else:
                self._set_up_context(namespace=namespace)
                self.init = True
                if create_new:
                    self.entity = self._generate_entity_node()
                else:
                    self.entity = None



    def _set_up_context(self, namespace):
        """
        Initializes Namespaces and JSON-LD context
        """
        self.context = {
            "rdfs": str(RDFS),
            "foaf": str(FOAF),
            "prov": str(PROV),
            "schema": str(SCHEMA),
            "provit": str(PROVIT)
        }
        self.namespace = PROVIT

    def _generate_entity_node(self):
        """
        Creates provenance entity URI
        """
        id_ = "{}/{}".format(self.file_name.replace(".", "_"), uuid.uuid4().hex)
        entity = URIRef("{}{}".format(self.namespace, id_))
        # add entity and entity location to graph
        self.graph.add((entity, RDF.type, PROV.Entity))
        self.graph.add((entity, PROV.atLocation, Literal(self.location)))
        return entity

    def _generate_agent_node(self, agent):
        """
        Creates provenance agent URI
        """
        #agent = URIRef("{}agent/{}".format(self.namespace, agent))
        agent = PROVIT[agent]
        # add agent to graph
        self.graph.add((agent, RDF.type, PROV.Agent))
        self.graph.add((self.entity, PROV.wasAttributedTo, agent))

    def _generate_activity_node(self, activity, desc, ended_at="", started_at=""):
        """
        Creates provenance activity URI
        """
        id_ = "{}/{}".format(activity, uuid.uuid4().hex)
        activity_uri = PROVIT[id_]

        self.graph.add((activity_uri, RDF.type, PROV.Activity))
        if type(desc) == str:
            self.graph.add((activity_uri, RDFS.label, Literal(desc)))

        if not ended_at:
            ended_at = datetime.now().isoformat()
        
        if started_at:
            print("add start time to graph")
            self.graph.add((activity_uri, PROV.startedAtTime, Literal(started_at, datatype="xsd:dateTime")))

        self.graph.add((activity_uri, PROV.endedAtTime, Literal(ended_at, datatype="xsd:dateTime")))
        self.graph.add((self.entity, PROV.wasGeneratedBy, activity_uri))


    def _get_root_entity(self):
        """
        Return the 'root' entity of the prov graph
        """
        # get all nodes of type prov:Entity
        entities = [s for s, p, o in self.graph.triples((None, RDF.type, PROV.Entity))]
        # get all entity nodes, which are sources
        derived = [o for s, p, o in self.graph.triples((None, PROV.wasDerivedFrom, None))]
        root = list(set(entities) - set(derived))

        if len(root) != 1:
            raise TypeError("Invalid provenance file: cannot locate root element")
        else:
            return root[0]


    def iter_remove(self, root_uri):

        #self.graph.add( (root_uri, PROVIT.status, PROVIT.removed) )
        source_uris = [ o for s, p, o in self.graph.triples( (root_uri, PROV.wasDerivedFrom, None) ) ]
        for source_uri in source_uris:
            self.iter_remove(source_uri)

        self.graph.remove( (root_uri, None, None) )


    def remove_last_event(self):
        """
        removes the last provenance event and all sources, if they do not belong to the same file
        """
        location = str(self.graph.value(self.entity, PROV.atLocation))

        #self.graph.add( (self.entity, PROVIT.status, PROVIT.removed) )
        source_uris = [ o for s, p, o in self.graph.triples( (self.entity, PROV.wasDerivedFrom, None) ) ]

        new_root_entity = None

        for source_uri in source_uris:
            source_location = str(self.graph.value(source_uri, PROV.atLocation))
            
            print(location, source_location)

            if location != source_location:
                self.iter_remove(source_uri)
            else:
                new_root_entity = source_uri

        self.graph.remove( (self.entity, None, None) )
        print(new_root_entity)
        self.entity = new_root_entity
        if not new_root_entity:
            self.graph = Graph()


    def add(self, agents, activity, description, started_at="", ended_at=""):
        """
        Add new basic provenance information (agent, activity) to file
        """
        if not self.entity:
            self.entity = self._generate_entity_node()

        if not self.init:
            # create new entity
            prior_entity = self.entity
            self.entity = self._generate_entity_node()
            # new prov entity is derived from old one
            self.graph.add((self.entity, PROV.wasDerivedFrom, prior_entity))

        # add prov information
        for agent in agents:
            print(agent)
            self._generate_agent_node(agent)
            # add prov information from agent profile, if available
            agent_profile = load_agent_profile(agent)
            if agent_profile:
                self.add_graph(agent_profile.graph())

        self._generate_activity_node(activity, description, ended_at, started_at)
        self.init = False


    def add_sources(self, filepaths, add_prov_to_source=True):
        """
        Add provenance information from source file (wasDerivedFrom) to provenance graph
        If source file does not have valid provenance data, a prov graph for the source file is initialized
        """
        if type(filepaths) == str:
            filepaths = [filepaths]
        if not type(filepaths) == list:
            raise TypeError
        else:
            for filepath in filepaths:
                if not os.path.exists(filepath):
                    raise IOError
                source_prov = Provenance(filepath)
                source_entity = source_prov.entity
                self.graph += source_prov.graph
                self.graph.add((self.entity, PROV.wasDerivedFrom, source_entity))

                if add_prov_to_source:
                    source_prov.save()


    def add_primary_source(self, primary_source, url=None, comment=None):
        """
        Adds primary source (+ url and comment) to provenance information
        """
        slug = primary_source
        primary_source = URIRef("{}{}".format(self.namespace, primary_source))
        self.graph.add((primary_source, RDF.type, PROV.PrimarySource))
        self.graph.add((self.entity, PROV.hadPrimarySource, primary_source))
        
        agent_profile = load_agent_profile(slug)
        if agent_profile:
            self.add_graph(agent_profile.graph())


    def add_graph(self, graph):
        self.graph = self.graph + graph


    def save(self):
        """
        Serializes prov graph as json-ld and saves it to file
        """
        with open(self.prov_filepath, "wb") as f:
            f.write(self.graph.serialize(format="json-ld", context=self.context))


    def __str__(self):
        raise NotImplementedError


    def __repr__(self):
        return "Provenance(\"{}\")".format(self.location)


    def _build_tree(self, root_entity):
        """
        Recursivly builds a tree dict with provenance information
        """
        tree = {}
        source_uris = [o for s, p, o in self.graph.triples((root_entity, PROV.wasDerivedFrom, None))]
        started_at = None
        # get provenance information
        location = [o for s, p, o in self.graph.triples((root_entity, PROV.atLocation, None))]
        print(root_entity, location)

        # agent
        agent = [o for s, p, o in self.graph.triples((root_entity, PROV.wasAttributedTo, None))]
        if len(agent) == 0:
            agent = [""]

        # status
        status_rv = [o for s, p, o in self.graph.triples((root_entity, PROVIT.status, None))]
        if len(status_rv) == 0:
            status = 'active'            
        else:
            status = 'removed'

        # activity
        activity = [o for s, p, o in self.graph.triples((root_entity, PROV.wasGeneratedBy, None))]
        if len(activity) > 0:
            ended_at = [o for s, p, o in self.graph.triples((activity[0], PROV.endedAtTime, None))]
            ended_at = str(ended_at[0])[:19].replace("T", " ")

            started_at = [o for s, p, o in self.graph.triples((activity[0], PROV.startedAtTime, None))]
            if len(started_at) > 0:
                started_at = str(started_at[0])[:19].replace("T", " ")
            else:
                started_at = None
            print(started_at," + ", ended_at)

            desc = [o for s, p, o in self.graph.triples((activity[0], RDFS.label, None))]

            primary_sources = []
            for s, p, o in self.graph.triples((root_entity, PROV.hadPrimarySource, None)):
                uri = str(o)
                slug = uri.split("/")[-1]
                url = [o2 for s2, p2, o2 in self.graph.triples((o, FOAF.homepage, None))]
                if len(url) > 0:
                    url = str(url[0])
                else:
                    url = ""
                comment = [o2 for s2, p2, o2 in self.graph.triples((o, RDFS.comment, None))]
                if len(comment) > 0:
                    comment = str(comment[0])
                else:
                    comment = ""

                primary_sources.append({
                    "uri": uri,
                    "url": url,
                    "slug": slug,
                    "comment": comment
                })

            # get sources data
            sources = []
            for source_uri in source_uris:
                source_data = self._build_tree(source_uri)
                sources.append(source_data)

            tree["uri"] = str(root_entity)
            tree["status"] = str(status)
            tree["agent"] = [ str(x) for x in agent ]
            tree["activity"] = str(activity[0])

            if started_at:
                tree["started_at"] = str (started_at)

            tree["ended_at"] = str(ended_at)
            tree["activity_desc"] = str(desc[0])
            tree["location"] = str(location[0])
            tree["primary_sources"] = primary_sources
            tree["sources"] = sources
        return tree


    def tree(self):
        """
        Returns of dict tree with provenance information
        """
        if self.entity:
            tree = self._build_tree(self.entity)
        else:
            tree = {}
        return tree

    def _get_uri_slug(self, uri):
        if "#" in uri:
            return str(uri).split("#")[-1]
        else:
            return str(uri).split("/")[-1]

    def _get_agent_data(self, agent_uri):

        
        slug = agent_uri.split("/")[-1]
        names = [ str(o) for s, p, o in self.graph.triples( (agent_uri, FOAF.name, None) ) ]
        homepage = [ str(o) for s, p, o in self.graph.triples( (agent_uri, FOAF.homepage, None) ) ]

        types = [ self._get_uri_slug(o) for s, p, o in self.graph.triples( (agent_uri, RDF.type, None ) ) ]
        print(types)

        if CF.PERSON in types:
            email = [ str(o) for s, p, o in self.graph.triples( (agent_uri, FOAF.mbox, None) ) ]
            institution = [ str(o) for s, p, o in self.graph.triples( (agent_uri, FOAF.member, None) ) ]
            return {
                "slug": slug,
                "uri": str(agent_uri),
                "type": CF.PERSON,
                "name": names,
                "homepage": homepage,
                "email": email,
                "institution": institution
            }
        elif CF.ORGANIZATION in types:
            return {
                "slug": slug,
                "uri": str(agent_uri),
                "type": CF.ORGANIZATION,
                "name": names,
                "homepage": homepage
            }
        elif CF.SOFTWARE in types:
            version = [ str(o) for s, p, o in self.graph.triples( (agent_uri, SCHEMA.softwareVersion, None) ) ]
            return {
                "slug": slug,
                "uri": str(agent_uri),
                "type": CF.SOFTWARE,
                "name": names,
                "homepage": homepage,
                "version": version
            }
        print(types, agent_uri)
        return None
        

    def get_agents(self, include_primary_sources=False):
        """
        Returns agent profiles from prov graph
        """

        agents = []

        agent_uris = [ s for s, p, o in self.graph.triples( (None, RDF.type, PROV.Agent ) ) ]

        if include_primary_sources:
            primary_source_uris = [ s for s, p, o in self.graph.triples( (None, RDF.type, PROV.PrimarySource ) ) ]
            agent_uris = list(set(agent_uris).union(set(primary_source_uris)))

        for agent_uri in agent_uris:
            agent_data = self._get_agent_data(agent_uri)
            agents.append(agent_data)

        return { x["slug"]:x for x in agents if x }


    def get_primary_sources(self):
        """
        Returns the URIs of all primary sources in prov graph
        """
        primary_sources = [str(o) for s, p, o in self.graph.triples((None, PROV.hadPrimarySource, None))]
        return list(set(primary_sources))
    

    def get_current_location(self):
        """
        Returs the file location of root element
        """
        return self.graph.value(self.entity, PROV.atLocation)
        