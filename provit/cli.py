"""
PROVIT command line client

Usage:

show provenance file information
$ provit [options] FILE_PATH

"""
import click
import json
import os
import sys

from prompt_toolkit.shortcuts import input_dialog, yes_no_dialog
from .agent import load_agent_profiles
from .prov import Provenance, load_prov
from .browser import start_provit_browser
from .home import add_directory


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
@click.option(
    "--agent", "-a", multiple=True, default="", help="Provenance information: agent"
)
@click.option("--activity", default="", help="Provenane information: activity")
@click.option(
    "--comment",
    "-c",
    default="",
    help="Provenance information: Description of the data manipulation process",
)
@click.option("--origin", "-o", default="", help="Provenance information: Data origin")
@click.option(
    "--sources",
    "-s",
    multiple=True,
    default="",
    help="Provenance information: Source files",
)
def add(filepath, agent, activity, comment, sources, origin):
    if not os.path.exists(filepath):
        print("Invalid filepath")
        sys.exit(1)

    prov = Provenance(filepath)
    if agent or activity or comment:
        if agent and activity and comment:
            prov.add(agents=agent, activity=activity, description=comment)
            prov.save()
        else:
            print("agent, activity and comment must be used together")
            sys.exit(1)

    if sources:
        for source in sources:
            prov.add_sources(source)
        prov.save()

    if origin:
        prov.add_primary_source(origin)

        prov.save()

@cli.command()
@click.argument("filepath")
def show(filepath):
    """
    Display the provenance tree of the given file. This is just another representation of the 
    provenance information stored in the provenance file. It resembles the internal data 
    structures of provit better, and probably also is more readable for humans. 

    This output is json, and formatted such that it can be processed further, e.g. in jq 
    to get coloured output.

    Example usage:

    $ provit show test.txt | jq
    """
    prov = load_prov(filepath)
    if prov:
        print(json.dumps(prov.tree(), indent=4))
    else:
        print(f"No provenance information found for {filepath}")
        print(f"You can create provenance for this file by typing: provit create {filepath}")
        sys.exit(1)


@cli.command()
@click.argument("filepath")
def create(filepath):
    
    # Activity
    prov = load_prov(filepath) 
    if prov:
        prompt_text = "Create a new provenance file."
    else:
        prompt_text = "Append a new provenance node to an existing file."
    activity = input_dialog(
        title="Activity (prov:wasGeneratedBy)",
        text=f"{prompt_text}\n\nEnter the perfomed activity:"
    )
    description = input_dialog(
        title="Comment / Description (rdfs:label for prov:Activity)",
        text=f"Describe the perfomed activity briefly:"
    )
   
    # Agent
    known_agents = load_agent_profiles() 
    known_agent_list = "\n".join([ a.slug for a in known_agents])
    result = yes_no_dialog(
        title="Select an agent (prov:Agent)",
        text=f"Known agents:\n{known_agent_list}\n\nDo you want to use a known agent?"
    ) 

    # Sources
    sources = []
    sources_prompt_title = "Source Files (prov:wasDerivedFrom)"
    while True:
        result = yes_no_dialog(
            title=sources_prompt_title,
            text="Do you want to add a(nother) source?"
        ) 
        if not result:
            break
        source = input_dialog(
            title=sources_prompt_title,
            text="Enter the filenames of the source files:"
        )
        sources.append(source)

    # Origin
    origin_prompt_title = "Origin (prov:hadPrimarySource)"
    result = yes_no_dialog(
        title=origin_prompt_title,
        text="Do you want to add an origin (primary source)?"
    )
    if result:
        origin = input_dialog(
            title=sources_prompt_title,
            text="Describe the perfomed activity briefly:"
        )
    else:
        origin = None

    print(activity)
    print(agent)
    print(description)
    print(sources)
    print(origin)

    
    
