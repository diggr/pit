import os
from .utils import walk_up

def init_dir():
    """
    Creates .pit file in directory root with costum directory uri
    """
    directory_uri = input("Identifier for current directory: ")
    with open(".pit", "w") as f:
        f.write(directory_uri)

def load_config(filepath):
    """
    Returns directory and content of cosest .pit file
    """
    for directory in walk_up(filepath):
        filepath = os.path.join(directory, ".pit")
        if os.path.exists(filepath):
            with open(filepath) as f:
                config = f.read()
            return directory, config
    return (None, None)

def pit_filepath (filepath):
    root_dir, config = load_config(filepath)
    
    if not root_dir:
        return os.path.abspath(filepath)

    rel_path = os.path.relpath(filepath, root_dir)
    #print(config, rel_path)
    return "{}:{}".format(config, rel_path)     