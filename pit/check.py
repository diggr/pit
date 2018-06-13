import os
from .prov import Provenance
from .config import pit_filepath

def check_file(filepath, pit_path=None):
    print("")
    prov_filepath = "{}.prov".format(filepath)
    pit_path = pit_filepath(filepath)

    print("File: {}".format(pit_path))
    if not os.path.exists(prov_filepath):
        print("\t NO PROVENACNE FILE")
    else:
        print("\t Checking Provenance:")
        prov = Provenance(filepath)

        # check file location
        prov_location = prov.get_current_location()
       
        if str(prov_location) == str(pit_path):
            print("\t ... check file location: OKAY")
        else:
            print("\t ... check file location: INCORRECT")
            add = input("\t\t Add copy information to provenance? [y/n] ")
            if add == "y":
                agent = input("\t\t Agent: ")
                prov.add(
                    agent=agent,
                    activity="move_file",
                    description="file moved to new location")
                prov.save()

        # check sources




def check_dir(directory):

    abs_path = os.path.abspath(directory)
    
    for filename in os.listdir(abs_path):

        # ignore directories
        if os.path.isdir(filename):
            continue

        # ignore hidden or prov files
        if filename.startswith(".") or filename.endswith(".prov"):
            continue

        filepath = os.path.join(abs_path, filename)
        check_file(filepath)