import os
import sys
import time
import webbrowser
import logging

from blinker import Signal
from ..prov import load_prov

from flask import Flask, jsonify, render_template
app = Flask(__name__)

# Disable all console logging
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

STD_DIR = "."
PROVIS_PORT = 5555

def path(filename):
    return os.path.join(STD_DIR, filename)

@app.route("/<filename>")
def display_file_prov(filename):
    abs_dir = os.path.abspath(STD_DIR)
    filepath = os.path.join(abs_dir, filename)

    if os.path.exists(filepath):
        prov = load_prov(os.path.join(abs_dir, filename))

        if prov:
            prov = prov.tree()

        return render_template("file_prov.html", abs_dir=abs_dir, filename=filename, prov=prov)
    else:
        return jsonify({"error": "file does not exist"})

@app.route('/')
def rootdirectory():

    abs_dir = os.path.abspath(STD_DIR)

    if os.path.exists(STD_DIR):
        directory = os.listdir(STD_DIR)

        directories = [ x for x in directory if os.path.isdir(path(x)) ]
        files = [ x for x in directory if os.path.isfile(path(x)) and x.split(".")[-1] != "prov" ]

        provs = []
        for f in files:
            prov = load_prov(path(f))
            #branches = prov.process_counts()
            if prov:
                origins = prov.get_primary_sources()
                origins = [ x.split("/")[-1] for x in origins ]
            else:
                origins = None
            if prov:
                prov = prov.tree()

            provs.append({
                "name": f,
                "prov": prov,
                "origins": origins
            })

        return render_template("dir.html", abs_dir=abs_dir, files=provs)
    else:
        return jsonify({})


def start_provis(directory, debug=False):
    n = os.fork()
    if n>0:
        try:
            app.run(debug=debug, port=PROVIS_PORT, use_reloader=False)
        except OSError as e:
            print("Cannot start provis server.")
            sys.exit(1)
    else:
        time.sleep(1)
        webbrowser.open("http://localhost:{}".format(PROVIS_PORT))

