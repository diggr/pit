from pit.prov import Provenance

# prov = Provenance(filepath="testdata/test.csv")
# prov.add(agent="peter", activity="fetcher", description="some youtube data api call")
# prov.add_primary_source("youtube", url="http://www.youtube.com", comment="everybody knows it")
# prov.save()

prov = Provenance(filepath="testdata/test.csv")
# prov.add(agent="script", activity="mapping", description="awesome mapping script")
# prov.save()
print(repr(prov))
print(prov.get_primary_sources())