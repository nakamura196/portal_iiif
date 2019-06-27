import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import json
from PIL import Image
import glob

collections = ["tori", "gramphone", "kahei"]

for collection in collections:
    path = "../docs/data/"+collection

    files = glob.glob(path+"/*.json")

    coll = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@type": "sc:Collection",
        "manifests": [],
        "vhint": "use-thumb"
    }

    manifests = coll["manifests"]
    coll_label = ""

    for i in range(len(files)):
        file2 = files[i]

        with open(file2, 'r') as f:
           obj = json.load(f)
           
           manifests.append({
               "@context": "http://iiif.io/api/presentation/2/context.json",
               "@id": obj["@id"],
               "@type": "sc:Manifest",
               "label": obj["label"],
               "thumbnail": obj["thumbnail"]
           })
           
           if i == 0:
                coll_label = obj["within"]

    coll["@id"] = "https://nakamura196.github.io/portal_iiif/collection/"+collection+".json"
    coll["label"] = coll_label

    f2 = open("../docs/collection/"+collection+".json", 'w')
    json.dump(coll, f2, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))

           
