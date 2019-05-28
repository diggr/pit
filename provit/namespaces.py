from rdflib import Namespace
from .config import get_config

cfg = get_config()

PROV = Namespace("http://www.w3.org/ns/prov#")
SCHEMA = Namespace("http://schema.org/")
PROVIT = Namespace(cfg.base_uri.format(""))
