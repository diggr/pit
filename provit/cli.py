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

from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
from .agent import load_agent_profiles
from .prov import Provenance, load_prov
from .browser import start_provit_browser
from .home import add_directory

YES = ["y", "ye", "yes"]
NO = ["n", "no"]


class YesNoValidator(Validator):
    def validate(self, document):
        text = document.text.strip().lower()
        if text and text not in YES + NO:
            raise ValidationError(message="Please enter 'y(es)' or 'n(o)'")


def mapyesno(result):
    return True if result.strip().lower() in YES else False


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
    if filepath.endswith(".prov"):
        filepath = filepath[:-5]
    prov = load_prov(filepath)
    if prov:
        print(json.dumps(prov.tree(), indent=4))
    else:
        print(f"No provenance information found for {filepath}")
        print(
            f"You can create provenance for this file by typing: provit create {filepath}"
        )
        sys.exit(1)


@cli.command()
@click.argument("filepath")
def create(filepath):

    # Activity
    prov = load_prov(filepath)
    if prov:
        print("Append a new provenance node to an existing file.")
    else:
        print("Create a new provenance file.")
        prov = Provenance(filepath)
    print("Activity (prov:wasGeneratedBy)")
    activity = prompt("Name the perfomed activity: ")

    print("Comment / Description (rdfs:label for prov:Activity)")
    description = prompt(f"Describe the perfomed activity briefly: ")

    # Agent
    known_agents = load_agent_profiles()
    known_agents_list = "\n".join([a.slug for a in known_agents])
    agents = []
    while True:
        while True:
            agent = None
    
            print("Select an agent (prov:Agent)")
            agent_yesno_result = prompt(
                f"Known agents:\n{known_agents_list}\n\nDo you want to use a known agent? ",
                validator=YesNoValidator(),
            )
            agent_result = mapyesno(agent_yesno_result)
    
            if agent_result:
                enumerated_agents_list = "\n".join(
                    [f"({i}) {agent.slug}" for i, agent in enumerate(known_agents)]
                )
                print("Select an agent (prov:Agent)")
                agent_id = prompt(
                    f"Known agents:\n{enumerated_agents_list}\n\nEnter the number of the agent you want to use: "
                )
    
                try:
                    agent_id_int = int(agent_id)
                except (ValueError, TypeError):
                    continue
    
                try:
                    agent = known_agents[agent_id_int]
                    break
                except IndexError:
                    continue
            else:
                print("Enter an agent (prov:Agent)")
                new_agent_name = prompt("Enter the name of your (new) agent: ")
                break
        
        if agent is not None:
            agent_name = agent.slug
        else:
            agent_name = new_agent_name
        agents.append(agent_name)

        another_agent = prompt("Add another agent?", validator=YesNoValidator())
        another_agent_result = mapyesno(another_agent)
        if not another_agent_result:
            break
   
    # Sources
    sources = []
    print("Source Files (prov:wasDerivedFrom)")
    while True:
        source_yesno_result = prompt(
            "Do you want to add a(nother) source?", validator=YesNoValidator()
        )
        if not mapyesno(source_yesno_result):
            break
        source = prompt("Enter the filenames of the source files: ")
        sources.append(source)

    # Origin
    print("Origin (prov:hadPrimarySource)")
    origin_yesno_result = prompt(
        "Do you want to add an origin (primary source)?", validator=YesNoValidator()
    )
    if mapyesno(origin_yesno_result):
        origin = prompt("Name the primary source (e.g. an URL, an agent, ...): ")
    else:
        origin = None

    prov.add(agents=agents, activity=activity, description=description)
    prov.save()

    if sources:
        for source in sources:
            prov.add_sources(source)
        prov.save()

    if origin:
        prov.add_primary_source(origin)
        prov.save()
