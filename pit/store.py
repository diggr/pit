
import json, csv, os
from datetime import datetime
from copy import deepcopy
from .prov import Provenance

def load_json(path):
    """ loads json file into data store object and checks if provenance information is available """
    full_path = os.path.abspath(path)
    if not os.path.exists(path):
        raise OSError("File does not exist")

    with open(path) as f:
        js = json.load(f)
    if "prov" in js and "data" in js:
        return Store(data=js["data"], **js["prov"])
    else:
        return Store(js, origin=full_path)

def load_csv(path, sep=","):
    """ loads csv into data store object and checks if provenance file exists """
    full_path = os.path.abspath(path)
    if not os.path.exists(path):
        raise OSError("File does not exist")

    prov_path = path+".prov"
    prov = None
    if os.path.exists(prov_path):
        with open(prov_path) as f:
            prov = json.load(f)

    with open(path) as f:
        csvreader = csv.DictReader(f)

        csvdata = [ dict(row) for row in csvreader ]
        if prov:
            return Store(data=csvdata, dtype="csv", **prov)
        else:
            return Store(data=csvdata, dtype="csv", origin=full_path)

#couch db functionality -- add at later point
def load_couch_doc(db, doc):
    """ loads data and prov informaton from couch db """
    """
    if db:
        if doc in db:
            prov = None
            data = None
            
            d = db[doc]
            if "prov" in d:
                prov_data = d["prov"]
                prov = Provenance(**prov_data)
            if "data" in d:
                data = d["data"]
            if prov and data:
                return Store(data=data, **prov.to_json())
            elif data:
                return Store(data=data, origin="couchdb:"+str(db.name)+"/"+str(doc))
        else:
            return None
    return None"""
    raise NotImplementedError

class Store():
    """
    Datastore class, containing both data and provenance information

    :_prov:   provenance information for data object
    :_data:   data of data object
    :_dtype:  type of data ojbect (at the moment just json)
    """

    def __init__(
        self, 
        data, 
        dtype="json", 
        origin=None, 
        sources=None, 
        agent=None, 
        desc=None, 
        target=None, 
        date=datetime.now().isoformat()
    ):
        self._prov = Provenance(origin=origin, sources=sources, agent=agent, desc=desc, date=date, target=target)
        self._dtype = dtype
        self._data = deepcopy(data)

    def set_prov(self, prov):
        self._prov = deepcopy(prov)

    def set_prov(
        self, 
        origin=None, 
        sources=None, 
        agent=None, 
        desc=None, 
        date=datetime.now().isoformat()
    ):
        """  set/reset provenance information for data object """
        if origin == None:
            origin = self._prov.get_origin()    
        self._prov = Provenance(origin=origin, sources=sources, agent=agent, desc=desc, date=date)

    def data(self):
        """ returns a copy of the data in the data store """
        return deepcopy(self._data)

    def prov(self):
        """ returns a copy of the provenance information """
        return deepcopy(self._prov.to_json())

    def print_prov(self, title=""):
        """ prints provenance information as a tree in the terminal """
        self._prov.print_tree(title)

    def save_to(self, path):
        """ writes data store object to file system """
        full_path = os.path.abspath(path)
        self._prov.set_target(full_path)

        if self._dtype == "json":
            output = {
                "data": self._data,
                "prov": self._prov.to_json()
            }
            with open(path, "w") as f:
                json.dump(output, f)
        elif self._dtype == "csv":
            prov_path = path+".prov"
            with open(path, "w") as f:
                writer = csv.writer(f)
                data = self._data

                writer.writerow(data[0].keys())

                for row in data:
                    writer.writerow([ value for key, value in row.items() ])
            with open(prov_path, "w") as f:
                json.dump(self._prov.to_json(), f)
    
    def save_to_couch(self, db, doc):
        """ add later"""
        """
        target = "couchdb:{}/{}".format(db.name, doc)
        self._prov.set_target(target)

        if doc in db:
            del db[doc]

        db.save({
            "_id": doc,
            "data": self._data,
            "prov": self._prov.to_json()
        })"""
        raise NotImplementedError

    def prov_to_rdf(self, path="prov.ttl", img=False):
        """ convertes provenance information """
        rdf = self._prov.save_to_rdf(path, img=img)