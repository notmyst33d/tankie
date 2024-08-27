import sys
import json
from bs4 import BeautifulSoup

with open(sys.argv[1], "r") as f:
    data = f.read()

converted_library = {"groups": {}}
xml = BeautifulSoup(data, features="xml")
library = xml.find("library")

converted_library["library_name"] = library["name"]
for group in library.find_all("prop-group"):
    converted_library["groups"][group["name"]] = []
    for prop in group.find_all("prop"):
        data = {"name": prop["name"]}

        if (sprite := prop.find("sprite")):
            data["sprite"] = {
                "file": sprite["file"],
                "origin_y": float(sprite["origin-y"]),
                "scale": float(sprite["scale"]),
            }

        if (mesh := prop.find("mesh")):
            data["mesh"] = mesh["file"].lower().replace(".3ds", ".glb")
            data["textures"] = [{"name": texture["name"], "diffuse_map": sys.argv[1].split("/")[-2] + "_" + texture["diffuse-map"].replace(".jpg", "_custom.png")} for texture in mesh.find_all("texture")]

        converted_library["groups"][group["name"]].append(data)

with open(sys.argv[1].replace(".xml", ".json"), "w") as f:
    f.write(json.dumps(converted_library))

