import os
import sys
import json

with open(f"{sys.argv[1]}/library.json", "r") as f:
    data = json.loads(f.read())

used_meshes = []
used_textures = []

for group in data["groups"].values():
    for prop in group:
        if prop.get("mesh") == None:
            continue
        used_textures.extend([texture["diffuse_map"] for texture in prop["textures"]])
        if prop["mesh"] not in used_meshes:
            used_meshes.append(prop["mesh"])

for entry in os.listdir(sys.argv[1]):
    if (entry.endswith(".3ds") or entry.endswith(".glb")) and entry not in used_meshes:
        print(f"Removing unused mesh {entry}")
        os.remove(f"{sys.argv[1]}/{entry}")

    if entry.endswith(".jpg") and entry not in used_textures:
        print(f"Removing unused texture {entry}")
        os.remove(f"{sys.argv[1]}/{entry}")

try:
    os.remove(f"{sys.argv[1]}/library.xml")
    os.remove(f"{sys.argv[1]}/images.xml")
except:
    pass
