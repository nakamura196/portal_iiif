import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import json
from PIL import Image
import glob


path = "../docs/collection"

files = glob.glob(path+"/*.json")

coll = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@type": "sc:Collection",
    "collections": []
}

collections = coll["collections"]

for i in range(len(files)):
    file2 = files[i]

    with open(file2, 'r') as f:
        obj = json.load(f)
        
        collections.append({
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": "https://nakamura196.github.io/portal_iiif/collection/"+obj["@id"].split("/")[-1],
            "@type": "sc:Collection",
            "label": obj["label"]
        })
coll["@id"] = "https://nakamura196.github.io/portal_iiif/collection.json"
coll["label"] = "UTokyo Academic Archives Portal Collection 2"

f2 = open("../docs/collection.json", 'w')
json.dump(coll, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

           
