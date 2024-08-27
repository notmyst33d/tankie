#!/usr/bin/bash
export HIRES_PREFIX=$(basename $1)
python convert_library.py $1/library.xml
for file in $1/*.3ds; do ./target/release/tankie $file; done
