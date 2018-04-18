from pit.prov import Provenance
import pprint

pp = pprint.PrettyPrinter(indent=2)

prov = Provenance("/home/pmuehleder/code/kirby/data/company_dataset.json")
#prov.add(agent="yt-fetcher", activity="fetch", description="fetching via youtube data api")
#prov.add_primary_source("youtube", "http://www.youtube.com", "you know it")
#prov.add_sources("testdata/yada.txt")
#prov.save()
print(prov._generate_entity_node())
#pp.pprint(prov.tree())
