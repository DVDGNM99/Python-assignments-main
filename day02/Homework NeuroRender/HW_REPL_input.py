"""
REPL input version of the BrainRender visualization script.
In lines CHANGE HERE you can change the acronyms of the brain regions
to visualize different areas.
"""

from brainglobe_atlasapi import BrainGlobeAtlas
from brainrender import Scene

def main():
    print(">> Downloading/using atlas 'allen_mouse_25um' (first time may take a few minutes)...")
    atlas = BrainGlobeAtlas("allen_mouse_25um")
    print("Atlas loaded:", atlas.metadata["name"], "| resolution:", atlas.resolution)
    print("Number of structures:", len(atlas.structures))

    # Create a scene and add brain regions
    scene = Scene(atlas_name="allen_mouse_25um")
    scene.add_brain_region("MOs", alpha=0.5, color="salmon")  # MOs = Secondary motor cortex CHANGE HERE
    scene.add_brain_region("VISp", alpha=0.3, color="skyblue")  # VISp = Primary visual cortex CHANGE HERE
    print(">> Opening 3D window... (close it to exit)")
    scene.render()

if __name__ == "__main__":
    main()
