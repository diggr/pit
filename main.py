from pit.store import Store, load_csv, load_json, load_couch_doc
#import couchdb
"""
original = load_csv("testdata/nodes.csv")
original.set_prov(agent="reading script", desc="node data set from another dimension")
original.save_to("testdata/test.csv")


data = load_csv("testdata/test.csv")

data2 = Store(data.data(), dtype="csv", sources=data.prov(), desc="whatever", agent="shittyscript")

data2.print_prov("Provenance for data 3")
data2.save_prov_rdf()
"""
couch = couchdb.Server()
db = couch["test"]

ostore = load_couch_doc(db, "test_1")
ostore.save_to_couch(db, "test_2")

store = load_couch_doc(db, "test_2")

#store.print_prov("couch test doc")

upper = Store(store.data()["title"].upper(), sources=store.prov(), desc="title to upper case", agent="upper case script")
upper.print_prov()
upper.save_to_couch(db, "test_2_upper")



"""
original = load_json("testdata/abc.json")
original.set_prov(desc="accessed via api", agent="peters script")
original.save_to("testdata/data4.json")

couch = couchdb.Server()
db = couch["test"]
db.save({
    "_id": "test_1",
    "data": original.data()
})

data = io.load_json("abc.json")
data2 = Store(data.data()["title"], sources=data.prov(), desc="reduction tot title", agent="step 2 script")

data3 = Store(data2.data().upper(), sources=[data2.prov(), original.prov()], desc="to upper", agent="upper script")
print(data3.data())
data3.print_prov()
data3.save_to("data3.json")
"""
#test = io.load_json("data3.json")
#test.print_prov()