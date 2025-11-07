# test_bg_render.py
from brainglobe_atlasapi import BrainGlobeAtlas
from brainrender import Scene

def main():
    print(">> Scarico/uso atlante allen_mouse_25um (prima volta può richiedere qualche minuto)...")
    atlas = BrainGlobeAtlas("allen_mouse_25um")
    print("OK atlas:", atlas.metadata["name"], "| risoluzione:", atlas.resolution)
    print("n. strutture:", len(atlas.structures))

    # crea una scena e aggiungi una regione
    scene = Scene(atlas_name="allen_mouse_25um")
    scene.add_brain_region("MOs", alpha=0.5, color="salmon")  # acronimo MOs = Secondary motor cortex
    scene.add_brain_region("VISp", alpha=0.3, color="skyblue") # visual cortex per esempio
    print(">> Apro finestra 3D... (chiudila per terminare)")
    scene.render()

if __name__ == "__main__":
    main()
