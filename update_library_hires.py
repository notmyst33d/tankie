import os
import sys
import shutil

hires = os.environ["HIRES"]
hires_ext = os.environ["HIRES_EXT"]
hires_prefix = sys.argv[1].split("/")[-1]

for entry in os.listdir(sys.argv[1]):
    if entry.endswith(".jpg"):
        hires_path = f"{hires}/{hires_prefix}_{entry.replace('.jpg', '_custom')}.{hires_ext}"
        if os.path.isfile(hires_path):
            shutil.copyfile(hires_path, f"{sys.argv[1]}/{entry}")
            print(f"{hires_path} -> {sys.argv[1]}/{entry}")
