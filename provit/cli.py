"""
PROVIT command line client

Usage:

show provenance file information
$ provit [options] FILE_PATH

"""

import click
import os
import pprint
import sys
from .prov import Provenance, load_prov
from .browser import start_provit_browser
from .home import add_directory
from .agent import load_agent_profile


@click.group()
def cli():
    pass


@cli.command()
@click.argument("directory", default="")
def browser(directory):
    if directory:
        if os.path.exists(directory):
            add_directory(os.path.abspath(directory))
        else:
            print("Invalid directory")
            sys.exit(1)
    start_provit_browser()


@cli.command()
@click.argument("filepath")
@click.option("--agent", "-a", multiple=True, default="", help="Provenance information: agent")
@click.option("--activity", default="", help="Provenane information: activity")
@click.option("--comment", "-c", default="", help="Provenance information: Description of the data manipulation process")
@click.option("--origin", "-o", default="", help="Provenance information: Data origin")
@click.option("--sources", "-s", multiple=True, default="", help="Provenance information: Source files")
def add(filepath, agent, activity, comment, sources, origin):
    if not os.path.exists(filepath):
        print("Invalid filepath")
        sys.exit(1)

    prov = Provenance(filepath)
    if agents and activity and comment:
        prov.add(agents=agents, activity=activity, description=comment)
        prov.save()

    if sources:
        for source in sources:
            prov.add_sources(source)
        prov.save()

    if origin:
        prov.add_primary_source(origin)

        prov.save()
