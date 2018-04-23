import os
import sys
from ..prov import load_prov

from flask import Flask, jsonify, render_template
app = Flask(__name__)

STD_DIR = "."

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
    app.run(debug=debug)

# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         STD_DIR = sys.argv[1]
#     app.run(debug=True)