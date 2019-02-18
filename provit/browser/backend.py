import os
import sys
import time
import webbrowser
import logging

from pathlib import Path
from multiprocessing import Process

from ..config import CONFIG as CF
from ..home import load_directories, remove_directories, add_directory
from ..agent import load_agent_profiles, load_agent_profile
from ..prov import Provenance, load_prov

from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Disable all console logging
''' app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True '''

PROVIS_PORT = 5555



# HOME VIEW (DIRECTORY LIST) 
@app.route('/directories', methods=['GET', 'POST'])
def directories():
    if request.method == 'GET':
        dirs = load_directories()
    elif request.method == 'POST':
        new_directory = request.json["directory"]
        dirs = add_directory(new_directory)

    return jsonify({
        "directories": dirs
    })


@app.route('/directories/remove', methods=['POST'])
def delete_directories():
    directory = request.json["directory"]
    dirs = remove_directories(directory)
    return jsonify({
        "directories": dirs
    })


# FILEBROWSER ENDPOINT 
@app.route('/filebrowser', methods=['POST'])
def file_browser():
    directory = request.json['directory']
    with_files = request.json['withFiles']
    with_hidden = request.json['withHidden']

    if directory == "" or not os.path.exists(directory):
        directory = str(Path.home())
        print("dir")
        print(directory)

    print(with_files)
    files = []
    dirs = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if not filename.endswith('.prov') and not os.path.isdir(filepath) and with_files:
            if not with_hidden and not filename.startswith('.'):
                files.append({
                    'filename': filename,
                    'filepath': filepath,
                })
        if os.path.isdir(filepath):
            if not with_hidden and not filename.startswith('.'):
                dirs.append({
                    'dirname': filename,
                    'dirpath': filepath 
                    })

    return jsonify({
        'files': sorted(files, key=lambda x: x['filename']),
        'dirs': sorted(dirs, key=lambda x: x['dirname'])
    })




# DIRECTORY VIEW (FILE LIST)

def files_with_prov(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if not filename.endswith(".prov") and not os.path.isdir(filepath):
            yield {
                "name": filename,
                "path": filepath
            }

def _build_file_list(directory):
    files = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if not filename.endswith(".prov") and not os.path.isdir(filepath):
            
            prov = None
            prov_file = "{}.prov".format(filepath)
            if os.path.exists(prov_file):
                print(prov_file)
                prov_data = Provenance(filepath)
                prov_tree = prov_data.tree()
                print(prov_tree)
                print(prov_data.get_primary_sources())
                prov = {
                    "last_activity": prov_tree["activity_desc"],
                    "last_agent": prov_tree["agent"],
                    "timestamp": prov_tree["ended_at"],
                    "last_location": prov_tree["location"]
                }

            files.append({
                "filename": filename,
                "filepath": filepath,
                "prov": prov
            })

    files = sorted(files, key=lambda x: x["filename"].lower())
    return files



@app.route('/directory', methods=['POST'])
def file_list():
    directory = request.json["directory"]

    files = _build_file_list(directory)

    return jsonify({
        "files": files
    })

@app.route('/directory/update', methods=['POST'])
def update_file_list():
    directory = request.json["directory"]

    for f in files_with_prov(directory):
        prov = Provenance(f["path"])
        if prov.tree()["location"] != f["path"]:
            prov.add(agents=[], activity="move_file", description="file moved to new location -> {}".format(directory))
            prov.save()

    files = _build_file_list(directory)
    return jsonify({
        "files": files
    })

# AGENTS LIST
@app.route("/agents")
def agent_list():
    agents = load_agent_profiles()
    agents_structured = { CF.PERSON: [], CF.SOFTWARE: [], CF.ORGANIZATION: []}
    for agent in agents:
        agents_structured[agent.type].append(agent.to_json())
    
    print(agents_structured.keys())
    return jsonify({
        "agents": agents_structured
    })



# FILE VIEW ENDPOINT
@app.route("/file", methods=['POST'])
def get_prov_data():
    filepath = request.json["filepath"] 
    prov = load_prov(filepath)

    if not prov:
        return jsonify({ "hasProv": False })
    return jsonify( {
        "hasProv": True,
        "root_event": prov.entity,
        "prov": prov.tree(),
        "agents": prov.get_agents()
    } )

@app.route("/file/remove", methods=["POST"])
def remove_prov_data():
    filepath = request.json["filepath"]
    prov = Provenance(filepath)
    prov.remove_last_event()
    prov.save()

    if not prov.entity:
        os.remove("{}.prov".format(filepath))

    prov = load_prov(filepath)

    if not prov:
        return jsonify({ "hasProv": False })
    return jsonify( {
        "hasProv": True,
        "root_event": prov.entity,
        "prov": prov.tree(),
        "agents": prov.get_agents()
    } )

@app.route("/file/add", methods=['POST'])
def add_prov_data():
    filepath = request.json["filepath"] 
    prov_data = request.json["prov"]
    is_timestamp = request.json["isTimestamp"]
    print("timestamp: ", is_timestamp)
    prov = Provenance(filepath)

    activity = prov_data["activitySlug"]
    agents = [ x for x in prov_data["agents"] if x ]
    desc = prov_data["comment"]
    sources = [ x for x in prov_data["sources"] if x ]
    primary_sources = [ x for x in prov_data["primarySources"] if x ]
    if is_timestamp:
        started_at = ""
        ended_at = prov_data["startedAt"]
    else:
        started_at = prov_data["startedAt"]
        ended_at = prov_data["endedAt"]

    prov.add(
        agents=agents,
        description=desc,
        activity=activity,
        started_at=started_at,
        ended_at=ended_at
    )

    prov.add_sources(sources)
    
    for primary_source in primary_sources:
        prov.add_primary_source(primary_source)

    prov.save()

    if not prov:
        return jsonify({})
    return jsonify( {
        "hasProv": True,
        "root_event": prov.entity,
        "prov": prov.tree(),
        "agents": prov.get_agents()
    } )


# CONFIG

@app.route('/config')
def config():
    provit_dir = CF.PROVIT_DIR
    return jsonify({
        "config": {
            "provit_dir": provit_dir
        }
    })


@app.route('/config/update')
def config_update():
    pass


#Provit browser routes
@app.route('/')
@app.route('/directory/')
@app.route('/agents/')
@app.route('/file/')
@app.route('/config/')
def index():
    return render_template("index.html")


#####
def start_backend(debug=False):
    try:
        app.run(debug=debug, port=PROVIS_PORT, use_reloader=False)
    except OSError as e:
        print("Cannot start provis server.")
        sys.exit(1)

def start_webbrowser():
    time.sleep(1)
    webbrowser.open("http://localhost:{}".format(PROVIS_PORT))

def start_provit_browser(debug=False):
    """
    Start provit backend and open webbrowser
    """
    backend_process = Process(target=start_backend, args=(debug,))
    backend_process.start()
    start_webbrowser()
