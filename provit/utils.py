#!/usr/bin/env python3

from rdflib import Graph
import json
import os
from itertools import combinations

from .config import get_config

cfg = get_config()


def provit_uri(slug):
    return cfg.base_uri.format(slug)


def load_jsonld(filepath):
    """
    Reads json-ld file and returns (rdfslib) graph and context
    """

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
