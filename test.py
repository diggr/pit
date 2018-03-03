from pit.prov import Provenance
import pprint

pp = pprint.PrettyPrinter(indent=2)

prov = Provenance("testdata/test.csv")
#prov.add(agent="yt-fetcher", activity="fetch", description="fetching via youtube data api")
#prov.add_primary_source("youtube", "http://www.youtube.com", "you know it")
#prov.add_sources("testdata/yada.txt")
#prov.save()
pp.pprint(prov.tree())
