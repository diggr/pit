#!/usr/bin/env python3

from rdflib import Graph
import json
import os
from itertools import combinations

from .config import CONFIG as CF

def combine_fields(record1, record2, field):
    if field not in record1:
        record1[field] = []
    if field not in record2:
        record2[field] = []

    returnset = list(set(record1[field]).union(set(record2[field])))
    return [x for x in returnset if x]

def update_dataset(record1, record2, fields):
    for field in fields:
        combined = combine_fields(record1, record2, field)
        if combined == []:
            record1.pop(field)



def combine_agents(agents1, agents2):
    for slug, data in agents2.items():
        if slug not in agents1:
            agents1[slug] = data
        else:
            update_dataset(agents1[slug], data, ["names", "institution", "homepage", "email"])

        if os.path.exists(CF.agent_profile_file(slug)):
            print(" ")
            print("yay")
            print("  ")

    return agents1


def provit_uri(slug):
    return CF.BASE_URI.format(slug)


def load_jsonld(filepath):
    """
    Reads json-ld file and returns (rdfslib) graph and context
    """

    print(filepath)
    if not os.path.exists(filepath):
        return (None, None)

    if os.path.getsize(filepath) == 0:
        return (None, None)

    with open(filepath) as f:
        file_data = json.load(f)

    # check for emtpy prov file
    if not file_data:
        return (None, None)

    if "@graph" in file_data:
        graph = file_data["@graph"]
    else:
        graph = file_data

    try:
        context = file_data["@context"]
    except Exception:
        raise IOError("JSON-LD Error: Context missing.")

    print(json.dumps(graph))

    g = Graph().parse(data=json.dumps(graph), format="json-ld", context=context)
    return (g, context)

def walk_up(start_dir):
    """
    Walks up directory tree from :start_dir: and returns directory paths
    """
    up_dir = os.path.abspath(start_dir)
    yield up_dir
    
    while up_dir != "/":
        up_dir = os.path.split(up_dir)[0]
        yield up_dir

