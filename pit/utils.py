from rdflib import Graph
import json

def load_jsonld(filepath):
    """
    Reads json-ld file and return (rdfslib) graph and context
    """
    with open(filepath) as f:
        file_data = json.load(f)
    graph = file_data["@graph"]
    context = file_data["@context"]
    g = Graph().parse(data=json.dumps(graph), format="json-ld", context=context)
    return (g, context)


