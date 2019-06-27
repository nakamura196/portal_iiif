import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import json
from PIL import Image

def get_thumbnal(img_url):
    return img_url

def create_manifest(manifest_uri, label, param, imgs):
    sequence_uri = manifest_uri+"/sequence/normal"

    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": manifest_uri,
        "@type": "sc:Manifest",
        "label": label,
        "sequences": [
            {
                "@id": sequence_uri,
                "@type": "sc:Sequence",
                "label": "Current Page Order",
                "viewingHint": "non-paged",
                "canvases": []
            }
        ]
    }

    for key in param:
        manifest[key] = param[key]

    width = -1
    height = -1

    canvases = manifest["sequences"][0]["canvases"]

    for i in range(len(imgs)):
        img_url = imgs[i]

        page = str(i + 1)

        canvas_uri = manifest_uri+"/canvas/p"+page

        tmp = {
            "@type": "sc:Canvas",
            "thumbnail": {},
            "images": [
                {
                    "@type": "oa:Annotation",
                    "motivation": "sc:painting",
                    "resource": {
                        "@type": "dctypes:Image",
                        "format": "image/jpeg",
                    }
                }
            ]
        }

        tmp["@id"] = canvas_uri
        tmp["label"] = "["+page+"]"

        tmp["thumbnail"]["@id"] = get_thumbnal(img_url)

        if i == 0:
            img = Image.open(urllib.request.urlopen(img_url))
            width, height = img.size

        tmp["images"][0]["resource"]["width"] = width
        tmp["images"][0]["resource"]["height"] = height

        tmp["width"] = width
        tmp["height"] = height

        anno_uri = manifest_uri+"/annotation/p"+page+"-image"

        
        tmp["images"][0]["@id"] = anno_uri
        

        tmp["images"][0]["resource"]["@id"] = img_url

        tmp["images"][0]["on"] = tmp["@id"]

        canvases.append(tmp)

    return manifest

def get_img_arr(soup):
    img_arr = []
    div = soup.find(class_="browse_cell_img")
    imgs = div.find_all("img")

    sp = url.split("/")[-1]
    prefix = "http://umdb.um.u-tokyo.ac.jp/DImt/Gramophone/JPG/"

    for i in range(len(imgs)):
        img = imgs[i]
        img_url = prefix+"/"+img.get("src").split("/")[-1]
        img_arr.append(img_url)
    return img_arr

def do_one(uri):
    

    res = urllib.request.urlopen(uri)
    # json_loads() でPythonオブジェクトに変換
    data = json.loads(res.read().decode('utf-8'))

    url = data["rdfs:seeAlso"][0]["@id"]
    id = data["@id"].split("/")[5].split("?")[0]
    label = data["dcterms:title"]
    metadata = []
    if "dcterms:description" in data:
        desc_arr = data["dcterms:description"]
        for desc in desc_arr:
            tmp = desc.split(": ")
            metadata.append({
                "label" : tmp[0],
                "value": tmp[1]
            })
    manifest_uri = url

    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    img_arr = get_img_arr(soup)

    param = {}
    param["metadata"] = metadata
    param["thumbnail"] = data["foaf:thumbnail"]["@id"]
    if "dcterms:rights" in data:
        param["license"] = data["dcterms:rights"][0]["@id"]
    param["attribution"] = data["dcndl:digitizedPublisher"][0]["@value"]
    param["logo"] = "https://iiif.dl.itc.u-tokyo.ac.jp/images/ut-logo.jpg"
    param["related"] = data["rdfs:seeAlso"][0]["@id"]
    param["seeAlso"] = data["@id"]
    param["within"] = data["dcterms:isPartOf"][0]["@value"]

    manifest = create_manifest(manifest_uri, label, param, img_arr)

    file = "../data/gramphone/"+id+".json"
    f2 = open(file, 'w')
    json.dump(manifest, f2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))

if __name__ == '__main__':

    loop_flg = True
    page = 0

    base_url = "https://da.dl.itc.u-tokyo.ac.jp/portal/search?collection=102&sort_by=field_title&_format=json"

    api_url = base_url+"&page="

    while loop_flg:
        url = api_url + str(
            page)
        print(url)

        page += 1

        res = urllib.request.urlopen(url)
        # json_loads() でPythonオブジェクトに変換
        data = json.loads(res.read().decode('utf-8'))

        for obj in data:
            do_one(obj["id"])

        if len(data) == 0:
            loop_flg = False

             


