"""
PIT command line client

Usage:

show provenance file information
pit <filepath> 

"""

import click
import os
import json
import sys
from pit.prov import Provenance, load_prov
import pprint


@click.command()
@click.option("--add", is_flag=True, help="Add provenance information layer to file")
@click.option("--agent", "-a", default="", help="Provenance information: agent")
@click.option("--activity", default="", help="Provenane information: activity")
@click.option("--desc", "-d", default="", help="Provenance information: Description of the data manipulation process")
@click.option("--origin", "-o", default="", help="Provenance information: Data origin")
@click.option("--sources", "-s", multiple=True, default="", help="Provenance information: Source files")
@click.argument("filepath")
def cli(agent, filepath, add, desc, activity, origin, sources):
    
    pp = pprint.PrettyPrinter(indent=1)

    if not os.path.exists(filepath):
        print("Invalid filepath")
        return 



    if not add:
        prov = load_prov(filepath)
        if not prov:
            print("No provenance Information available")
            return

    elif add:
        prov = Provenance(filepath)
        if agent and activity and desc:
            prov.add(agent=agent, activity=activity, description=desc)
            prov.save()

        if sources:
            for source in sources:
                prov.add_sources(source)
            prov.save()
        
        if origin:
            prov.add_primary_source(origin)
            prov.save()
        
    pp.pprint(prov.tree())
            
