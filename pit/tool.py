"""
PIT command line client

Usage:

show provenance file information
$ pit [options] FILE_PATH

"""

import click
import os
import pprint
import sys
from .prov import Provenance, load_prov, PROVIT_NS
from .provis.provis import start_provis


@click.command()
@click.option("--add", is_flag=True, help="Add provenance information layer to file")
@click.option("--agent", "-a", default="", help="Provenance information: agent")
@click.option("--activity", default="", help="Provenane information: activity")
@click.option("--desc", "-d", default="", help="Provenance information: Description of the data manipulation process")
@click.option("--origin", "-o", default="", help="Provenance information: Data origin")
@click.option("--sources", "-s", multiple=True, default="", help="Provenance information: Source files")
@click.option("--browser", "-b", is_flag=True, help="Provenance browser")
@click.option("--namespace", "-n", default=PROVIT_NS, help="Provenance Namespace, default: {}".format(PROVIT_NS))
@click.argument("filepath")
def cli(agent, filepath, add, desc, activity, origin, sources, browser, namespace):

    pp = pprint.PrettyPrinter(indent=1)

    if browser:
        start_provis(filepath, debug=True)
        sys.exit(0)

    if not os.path.isfile(filepath):
        if os.path.isdir(filepath):
            print("Filepath must point to a file, not a directory.")
        else:
            print("Invalid filepath.")
        return

    if not add:
        prov = load_prov(filepath, namespace=namespace)
        if not prov:
            print("No provenance Information available")
            return

    elif add:
        prov = Provenance(filepath, namespace=namespace)
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
