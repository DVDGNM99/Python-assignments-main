#!/usr/bin/env python3
"""
Build a complete JSON list of brain regions from the Allen Mouse Brain Atlas.

This script downloads the full structure graph (hierarchical tree) of the adult
mouse brain from the Allen Brain Map API, extracts every region’s acronym and
name, and saves them as a flat JSON dictionary.

Output file:
    regions_full.json

Example structure of the output file:
    {
        "MOs": "Secondary motor area",
        "VISp": "Primary visual area",
        "TH":  "Thalamus",
        ...
    }

The resulting JSON can be used by your BrainRender GUI to populate dropdown menus
with all available ARA regions.
"""

import json
import urllib.request

# URL of the complete Allen Mouse Brain Atlas structure graph (graph_id=1)
URL = "http://api.brain-map.org/api/v2/structure_graph_download/1.json"

# Download the data from the Allen API
with urllib.request.urlopen(URL) as response:
    data = json.load(response)

def walk(nodes, out):
    """
    Recursively traverse the hierarchical structure graph and
    collect all regions' acronyms and names into the output dictionary.
    """
    for node in nodes:
        acronym = node.get("acronym")
        name = node.get("name")
        if acronym and name:
            out[acronym] = name
        children = node.get("children") or []
        walk(children, out)

# The data is nested under 'msg' → [root node] → 'children'
root = data["msg"][0]
regions = {}
walk([root], regions)

# Save results to JSON
with open("regions_full.json", "w", encoding="utf-8") as f:
    json.dump(regions, f, ensure_ascii=False, indent=2)

print(f"Successfully wrote {len(regions)} regions to regions_full.json")
