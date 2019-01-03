from rdflib import Namespace
from .config import CONFIG as CF

PROV = Namespace("http://www.w3.org/ns/prov#")
PROVIT = Namespace(CF.BASE_URI.format(""))