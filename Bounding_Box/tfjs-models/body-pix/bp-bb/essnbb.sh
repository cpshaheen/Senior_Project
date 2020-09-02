#!/usr/bin/env bash

for d1 in essn_top/* ; do
    for d2 in "$d1"/
    do
        node bp_dir.js "$d2"
        wait $!
        python3 AnnotateTopDir.py "$d2"
    done
done