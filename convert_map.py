import sys
import json
from bs4 import BeautifulSoup

with open(sys.argv[1], "r") as f:
    data = f.read()

converted_map = {"static_geometry": []}
xml = BeautifulSoup(data, features="xml")
static_geometry = xml.find("static-geometry")

for prop in static_geometry.find_all("prop"):
    converted_map["static_geometry"].append({
        "name": prop["name"],
        "library_name": prop["library-name"],
        "group_name": prop["group-name"],
        "texture_name": prop.find("texture-name").text,
        "position": {
            "x": float(prop.find("position").find("x").text) / 100,
            "y": float(prop.find("position").find("z").text) / 100,  # y and z flip is intentional
            "z": -float(prop.find("position").find("y").text) / 100,  # And yes, this is also intentional, otherwise the level would be flipped
        },
        "rotation": {
            "x": float(x.text if (x := prop.find("rotation").find("x")) else 0.0),
            "y": float(z.text if (z := prop.find("rotation").find("z")) else 0.0),  # y and z flip is intentional
            "z": float(y.text if (y := prop.find("rotation").find("y")) else 0.0),
        }
    })

with open(sys.argv[1].replace(".xml", ".json"), "w") as f:
    f.write(json.dumps(converted_map))
