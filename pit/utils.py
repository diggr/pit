from rdflib import Graph
import json
import os

def load_jsonld(filepath):
    """
    Reads json-ld file and returns (rdfslib) graph and context
    """
    with open(filepath) as f:
        file_data = json.load(f)
    if "@graph" in file_data:
        graph = file_data["@graph"]
    else:
        graph = file_data
    context = file_data["@context"]
    g = Graph().parse(data=json.dumps(graph), format="json-ld", context=context)
    return (g, context)
