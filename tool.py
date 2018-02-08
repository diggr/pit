import click
import os
import json
import sys
#import couchdb
from pit.prov import Provenance

FILE = "file"
#COUCHDB = "couchdb"


def load_prov(filepath):
    """retrieve prov information from file"""
    prov = None
    filetype = filepath.split(".")[-1]
    if filetype == "json":
        with open(filepath) as f:
            data = json.load(f)
        if "prov" in data:
            prov = Provenance(**data["prov"])
    else:
        provfile = filepath+".prov"
        if not os.path.exists(provfile):
            click.echo("No provenance for file <{}> available".format(filepath))
        else:
            with open(provfile) as f:
                provdata = json.load(f)
            prov = Provenance(**provdata)
    return prov


@click.command()
@click.option("--rdf", default="", help="RDF export file for provenance infomration")
@click.option("--ns", default="http://pit/", help="Declare RDF namespace (default: http://pit/)")
@click.option("--img", is_flag=True, help="Saves provenance RDF information as png image")
@click.option("--add", is_flag=True, help="Add provenance information layer to file")
@click.option("--update", is_flag=True, help="Update current provenance information layer")
@click.option("--agent", "-a", default="", help="Provenance information: agent")
@click.option("--desc", "-d", default="", help="Provenance information: Description of the data manipulation process")
@click.option("--origin", "-o", default="", help="Provenance information: Data origin")
@click.option("--sources", "-s", multiple=True, default="", help="Provenance information: Source files")
@click.argument("filepath")
def cli(agent, filepath, add, desc, origin, sources, update, rdf, ns, img):
    
    modus = None

    src = []
    #sources prov 
    for s in sources:
        if os.path.exists(s):
            p = load_prov(s)
            if p:
                src.append(p.to_json())
            else:
                src.append(Provenance(target=os.path.abspath(s), date=None, desc="no provenance information available").to_json())
        else:
            raise FileNotFoundError("Source file <{}> does not exist".format(s))

    """ couchdb integration - add later
    # check if filepath = couchdb url
    if filepath[:8] == "couchdb:":

        modus = COUCHDB

        server = filepath.split("/")[0]
        server = server.replace("couchdb:", "http://")
        db = filepath.split("/")[-2]
        doc = filepath.split("/")[-1]

        try:
            couch = couchdb.Server(server)
        except:
            click.echo("Cannot connect to CouchDB <{}>".format(server))
            return None
        try:
            database = couch[db]
        except:
            click.echo("No database <{}>".format(db))
            return None
        try:
            document = database[doc]
        except:
            click.echo("No document <{}> in database <{}>".format(doc, db))
            return None

        
        if "prov" in document:
            prov = Provenance(**document["prov"])
        else:
            click.echo("No provenance information for document <{}> available".format(doc))
            prov = None

        full_path = filepath

    """
    # file 
    #elif not os.path.exists(filepath):
    if not os.path.exists(filepath): 
        click.echo("File <{}>  does not exist".format(filepath))
    else: 
        modus = FILE

        full_path = os.path.abspath(filepath)
        prov = load_prov(filepath)

    # add new provenance information
    if (add):

        if prov:
            prov = prov.to_json()
            src = [prov]+src
        if origin == "":
            origin = None
        if desc == "":
            desc = None
        
        if src == []: src = None
        elif len(src) == 1: src = src[0]

        if agent != "" or desc != "" or origin != "" or sources != []:
            prov = Provenance(agent=agent, desc=desc, origin=origin, sources=src, target=full_path)


        filetype = filepath.split(".")[-1]
        provfile = filepath+".prov"
        if filetype == "json":

            with open(filepath) as f:
                raw_data = json.load(f)
            data = {}
            data["data"] = raw_data

            data["prov"] = prov.to_json()
            with open(filepath, "w") as f:
                json.dump(data, f)
        else:
            with open(provfile, "w") as f:
                json.dump(prov.to_json(), f)

    
    # if available print prov information
    if prov:
        prov.print_tree(filepath)

    if not add and rdf != "":
        prov.save_to_rdf(rdf, img=img)


