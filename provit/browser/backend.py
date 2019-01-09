import os
import sys
import time
import webbrowser
import logging

from ..config import CONFIG as CF
from ..home import load_directories, remove_directories, add_directory
from ..agent import load_agent_profiles
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



# DIRECTORIES (DIRECTORY LIST) 

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


# DIRECTORY (FILE LIST)

@app.route('/directory', methods=['POST'])
def file_list():
    directory = request.json["directory"]
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
                    "timestamp": prov_tree["ended_at"]
                }

            files.append({
                "filename": filename,
                "filepath": filepath,
                "prov": prov
            })

    files = sorted(files, key=lambda x: x["filename"].lower())

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
    
    print(agents_structured)
    return jsonify({
        "agents": agents_structured
    })



# FILE ENDPOINT

@app.route("/file", methods=['POST'])
def get_prov_data():
    filepath = request.json["filepath"] 
    prov = load_prov(filepath)

    network = {
        "nodes": [],
        "edges": []
    }

    if not prov:
        return jsonify({})
    return jsonify( {
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


def start_browser(debug=True):
    n = os.fork()
    if n > 0:
        try:
            app.run(debug=debug, port=PROVIS_PORT, use_reloader=False)
        except OSError as e:
            print("Cannot start provis server.")
            sys.exit(1)
    else:
        time.sleep(1)
        webbrowser.open("http://localhost:{}".format(PROVIS_PORT))
