"""
Provenance class handles provenance metadata information.

Use:

from pit.prov import Provenance

#load prov data for a file, or create new prov for file
prov = Provenance(<filepath>)

#add provenance metadata
prov.add(agent="agent", activity="activity", description="...")
prov.add_priary_source("primary_source", url="http://...", comment="...")

#return provenance as json tree
prov.tree()

#save provenance metadata
prov.save()

"""

import json
import uuid
import os

from datetime import datetime
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, FOAF, RDFS

from .utils import load_jsonld

#Additional namespaces
PIT = {
    "entity": "http://pit.diggr.link/",
    "agent": "http://pit.diggr.link/agent#",
    "activity": "http://pit.diggr.link/act/"
}
PROV = Namespace("http://www.w3.org/ns/prov#")


class Provenance(object):
    """
    Provenance class handles the provenance metadata graph
    """
    graph = Graph()

    def _set_up_context(self):
        """
        Initializes Namespaces and JSON-LD context
        """
        self.context = { 
            "rdfs": str(RDFS),
            "prov": "http://www.w3.org/ns/prov#", 
            "pit_entity": PIT["entity"],
            "pit_agent": PIT["agent"],
            "pit_activity": PIT["activity"],
        }
        #print(self.context)

    def _generate_entity_node(self):
        """
        Creates provenance entity URI 
        """
        id_ = "pit_{}".format(uuid.uuid4().hex)
        entity = URIRef("{}{}".format(PIT["entity"], id_))
        #add entity and entity location to graph
        self.graph.add( (entity, RDF.type, PROV.Entity) )
        self.graph.add( (entity, PROV.atLocation, Literal(self.location)) ) 
        return entity

    def _generate_agent_node(self, agent):
        """
        Creates provenance agent URI
        """
        agent = URIRef("{}{}".format(PIT["agent"], agent))
        #add agent to graph
        self.graph.add( (agent, RDF.type, PROV.Agent) )
        self.graph.add( (self.entity, PROV.wasAttributedTo, agent) )    

    def _generate_activity_node(self, activity, desc):
        """
        Creates provenance activity URI
        """
        id_ =  "{}_{}".format(activity, uuid.uuid4().hex)
        activity = URIRef("{}{}".format(PIT["activity"], id_))
        #add activity to graph
        self.graph.add( (activity, RDF.type, PROV.Activity) )
        if type(desc) == str:
            self.graph.add( (activity, RDFS.label, Literal(desc)) ) 
        self.graph.add( (activity, PROV.endedAtTime, Literal(datetime.now().isoformat(), datatype="xsd:dateTime")) )
        self.graph.add( (self.entity, PROV.wasGeneratedBy, activity) )


    def _get_root_entity(self):
        #get all Nodes of type prov:Entity 
        entities = [ s for s,p,o in self.graph.triples( (None, RDF.type, PROV.Entity) ) ]
        derived =  [ o for s,p,o in self.graph.triples( (None, PROV.wasDerivedFrom, None) ) ]
        root = list(set(entities) - set(derived))
        if len(root) != 1:
            print("invalid provenance file")
        else:
            return root[0]
        
    def __init__(self, filepath):
        
        self._set_up_context()
        self.prov_filepath = "{}.prov".format(filepath)
        self.location = os.path.abspath(filepath)

        if not os.path.exists(self.prov_filepath):
            self.init = True
            #generate new entity
            self.entity = self._generate_entity_node()
        else:
            self.init = False
            #load and parse provenance json-ld file
            g, context = load_jsonld(self.prov_filepath)
            self.context = context
            self.graph = g
            #set root entity
            self.entity = self._get_root_entity()
            #print(self.entity)
            #print(g.serialize(format="json-ld", context=self.context))

    def add(self, agent, activity, description):
        """
        Add new basic provenance information (agent, activity) to file
        """
        if not self.init:
            #create new entity
            prior_entity = self.entity
            self.entity = self._generate_entity_node()
            #new prov entity is derived from old one
            self.graph.add( (self.entity, PROV.wasDerivedFrom, prior_entity))

        #add prov information
        self._generate_agent_node(agent)
        self._generate_activity_node(activity, description)
        self.init = False

    def add_source(self, filepath):
        raise NotImplementedError

    def add_primary_source(self, primary_source, url=None, comment=None):
        """
        Adds primary source (+ url and comment) to provenance information
        """
        primary_source = URIRef("{}{}".format(PIT["entity"], primary_source))
        self.graph.add( (primary_source, RDF.type, PROV.PrimarySource) )
        self.graph.add( (self.entity, PROV.hadPrimarySource, primary_source ) ) 

        if comment:
            self.graph.add( (primary_source, RDFS.comment, Literal(comment)) )
        if url:
            self.graph.add( (primary_source, FOAF.homepage, Literal(url)) )
        
    def save(self):
        with open(self.prov_filepath, "wb") as f:
            f.write(self.graph.serialize(format="json-ld", context=self.context))

    def __str__(self):
        pass
    
    def __repr__(self):
        return "Provenance(\"{}\")".format(self.location)

    def get_primary_sources(self):
        primary_sources = [ str(o) for s,p,o in self.graph.triples( (None, PROV.hadPrimarySource, None) ) ]
        return list(set(primary_sources))
        
