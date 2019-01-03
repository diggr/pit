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
from .browser import start_browser
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
    start_browser()

@cli.command()
@click.argument("filepath")
@click.option("--agents", "-a", multiple=True, default="", help="Provenance information: agent")
@click.option("--activity", default="", help="Provenane information: activity")
@click.option("--comment", "-c", default="", help="Provenance information: Description of the data manipulation process")
@click.option("--origin", "-o", default="", help="Provenance information: Data origin")
@click.option("--sources", "-s", multiple=True, default="", help="Provenance information: Source files")
def add(filepath, agents, activity, comment, sources, origin):
    if not os.path.exists(filepath):
        print("Invalid filepath")
        sys.exit(1)

    prov = Provenance(filepath)
    if agents and activity and comment:
        prov.add(agents=agents, activity=activity, description=comment)
        prov.save()

        for agent in agents: 
            agent_profile = load_agent_profile(agent)
            if agent_profile:
                prov.add_graph(agent_profile.graph())
                prov.save()

    if sources:
        for source in sources:
            prov.add_sources(source)
        prov.save()

    if origin:
        prov.add_primary_source(origin)

        agent_profile = load_agent_profile(origin)
        if agent_profile:
            prov.add_graph(agent_profile.graph())


        prov.save()


''' @click.command()
@click.option("--init", "-i", is_flag=True, help="Add provenance configuration for current directory")
@click.option("--check", "-c", is_flag=True, help="Checks provenance of all files in directory")
@click.option("--add", is_flag=True, help="Add provenance information layer to file")
@click.option("--agent", "-a", default="", help="Provenance information: agent")
@click.option("--activity", default="", help="Provenane information: activity")
@click.option("--desc", "-d", default="", help="Provenance information: Description of the data manipulation process")
@click.option("--origin", "-o", default="", help="Provenance information: Data origin")
@click.option("--sources", "-s", multiple=True, default="", help="Provenance information: Source files")
@click.option("--browser", "-b", is_flag=True, help="Provenance browser")
@click.option("--namespace", "-n", default=PROVIT_NS, help="Provenance Namespace, default: {}".format(PROVIT_NS))
@click.argument("filepath", required=False)
def cli(agent, init, check, filepath, add, desc, activity, origin, sources, browser, namespace):

    pp = pprint.PrettyPrinter(indent=1)

    if browser:
        start_provis(filepath, debug=True)
        sys.exit(0)

    if init:
        init_dir()
        #print(load_config())

    if check:
        check_dir(".")

    if filepath:
        if not os.path.isfile(filepath):
            if os.path.isdir(filepath):
                print("Filepath must point to a file, not a directory.")
                sys.exit(1)
            else:
                print("Invalid filepath.")
                sys.exit(2)

        if not add:
            prov = load_prov(filepath, namespace=namespace)
            if not prov:
                print("No provenance Information available")
                sys.exit(0)

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
 '''