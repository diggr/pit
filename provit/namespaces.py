from rdflib import Namespace
from .config import CONFIG as CF

PROV = Namespace("http://www.w3.org/ns/prov#")
SCHEMA = Namespace("http://schema.org/")
PROVIT = Namespace(CF.BASE_URI.format(""))