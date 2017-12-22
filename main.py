from pit.store import Store, load_csv, load_json

original = load_csv("testdata/nodes.csv")
original.set_prov(agent="reading script", desc="node data set from another dimension")
original.save_to("testdata/test.csv")


data = load_csv("testdata/test.csv")

data2 = Store(data.data(), dtype="csv", sources=data.prov(), desc="whatever", agent="shittyscript")

data2.print_prov("Provenance for data 3")
data2.save_prov_rdf()




"""
original = io.load_json("test.json")
original.set_prov(desc="accessed via api", agent="peters script")
original.save_to("abc.json")

data = io.load_json("abc.json")
data2 = Store(data.data()["title"], sources=data.prov(), desc="reduction tot title", agent="step 2 script")

data3 = Store(data2.data().upper(), sources=[data2.prov(), original.prov()], desc="to upper", agent="upper script")
print(data3.data())
data3.print_prov()
data3.save_to("data3.json")
"""
#test = io.load_json("data3.json")
#test.print_prov()