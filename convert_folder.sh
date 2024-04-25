#!/usr/bin/bash
python convert_library.py $1/library.xml
for file in $1/*.3ds; do cargo run -- $file; done
