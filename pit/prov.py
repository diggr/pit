import json
from copy import deepcopy
from datetime import datetime
from prov.model import ProvDocument
import uuid
from urllib.parse import quote
from prov.dot import prov_to_dot

def validate_prov(        
    origin=None, 
    sources=None, 
    target=None, 
    agent=None, 
    desc=None, 
    date=datetime.now().isoformat()
):
    """ check if provenance data is valid """
    valid_info = 0
    if origin:
        if type(origin) != str:
            raise TypeError("<origin> has to be string")
        valid_info += 1
    if desc:
        if type(desc) != str:
            raise TypeError("<desc> has to be string")
        valid_info += 1
    if sources:
        if type(sources) == list:
            for source in sources:
                p = validate_prov(**source)
        elif type(sources) == dict:
            p = validate_prov(**sources)
        else:
            raise TypeError("<sources> not valid data")
        valid_info += 1
    if target:
        if type(target) != str:
            raise TypeError("<target> hs to be string")
        valid_info += 1
    if agent:
        if type(agent) != str:
            raise TypeError("<aggent> hs to be string") 
        valid_info += 1
    
    # todo: check date format

    #no valid provenance information available
    if valid_info == 0:
        raise ValueError("No valid provenance information")

    return True

class Provenance():
    """
    Class containing provenance information

    :origin:    original data source  (API, file)
    :sources:   provenance information from source data objects
    :target:    persistent target of data object (e.g. file)
    :agent:     agent handling the data object (e.g. script, user)
    :desc:      short description of the data manipulation process
    :date:      timestamp
    """

    def __init__(
        self, 
        origin=None, 
        sources=None, 
        target=None, 
        agent=None, 
        desc=None, 
        date=None
    ):

        if validate_prov(origin, sources, target, agent, desc, date):
            
            if not date:
                date = datetime.now().isoformat()

            self.origin = origin
            self.sources = deepcopy(sources)
            self.target = target
            self.agent = agent
            self.desc = desc
            self.date = date

    def set_target(self, target):
        """ set target """
        self.target = target

    def get_origin(self):
        return self.origin

    def to_json(self):
        """ returns povenance information as json/dict """
        output = {
            "origin": self.origin,
            "sources": deepcopy(self.sources),
            "target": self.target,
            "agent": self.agent,
            "desc": self.desc,
            "date": self.date
        }
        return output
 
    def _print_element(self, base, elem, data):
        """ prints a provenance element if available """
        if data != None:
            if elem in data:
                if data[elem] != None:
                    print("{base}{elem}: {value}".format(base=base, elem=elem, value=data[elem]))

    def _print_prov(self, data, base=" |- "):
        """ prints a level of provenance information """
        print(base[:len(base)-2])
        self._print_element(base, "origin", data)
        self._print_element(base, "agent", data)
        self._print_element(base, "date", data)
        self._print_element(base, "desc", data)
        self._print_element(base, "target", data)
        if data:
            if data["sources"] != None:
                print("{base}Sources:".format(base=base))
                if type(data["sources"]) == list:
                    for source in data["sources"]:
                        self._print_prov(source, base="\t" +base)

                else:
                    self._print_prov(data["sources"], base="\t" +base)

    def _generate_uri(self, ns, value):

        value = value.replace(" ", "_")
        value = quote(value)
        uri = "{}:{}".format(ns, value)
        return uri


    def _pit_uuid(self):
        _id = "pit_{}".format(uuid.uuid4().hex)
        return _id

    def _json_to_rdf(self, data, provdoc, root_entity):
        """ recursively iterates through prov data and add information to provdoc """
        if data: 
            #entity
            label = "None"
            if "target" in data:
                label = data["target"]
            _id = self._pit_uuid()
            src_entity = provdoc.entity(self._generate_uri("data", _id), {"prov:label": label})
            if root_entity:
                provdoc.wasDerivedFrom(root_entity, src_entity)

            #agent
            agent = None
            if "agent" in data:
                agent = data["agent"]
            if agent:
                src_agent = provdoc.agent(self._generate_uri("agent", agent))
                provdoc.wasAttributedTo(src_entity, src_agent)

            #activity
            desc = "None"
            if "desc" in data:
                desc = data["desc"]
            end = None
            if "date" in data:
                end = data["date"]
            _id = self._pit_uuid()
            src_activity =provdoc.activity(self._generate_uri("activity", _id), endTime=end, other_attributes={"prov:label": desc})
            provdoc.wasGeneratedBy(src_entity, src_activity)

            #origin - primary source
            origin = "None"
            if "origin" in data:
                origin = data["origin"]
                if origin:
                    _id = self._pit_uuid()
                    primary_source = provdoc.entity(self._generate_uri("data", _id),  {"prov:label": origin})
                    provdoc.hadPrimarySource(src_entity, primary_source)

            #sources
            if "sources" in data:
                if type(data["sources"]) == list:
                    for source in data["sources"]:
                        provdoc = self._json_to_rdf(source, provdoc, src_entity)
                else:
                    provdoc = self._json_to_rdf(data["sources"], provdoc, src_entity)

        return provdoc        

    def save_to_rdf(
        self, 
        filename="prov.ttl",
        data_ns="http://pit.example.com/datapoints/", 
        agent_ns="http://pit.example.com/agents/", 
        activity_ns="http://pit.example.com/activities/",
        img=False
    ):
        """ converts provenance data into rdf """
        provdoc = ProvDocument()
        provdoc.add_namespace("data", data_ns)
        provdoc.add_namespace("agent", agent_ns)
        provdoc.add_namespace("activity", activity_ns)

        data = self.to_json()
        self._json_to_rdf(data, provdoc, None)

        #export rdf prov as image
        if img:
            dot = prov_to_dot(provdoc)
            img_file = filename.replace(".ttl", ".png")
            dot.write_png(img_file)

        provdoc.serialize(filename, format="rdf", rdf="ttl")
    
    def print_tree(self, title=""):
        """ recursevly prints provenance information as tree"""
        print(title)
        self._print_prov(self.to_json())

    def __str__(self):
        raise NotImplementedError
    
    def __repr__(self):
        raise NotImplementedError
