
"""
CLI input version of the BrainRender visualization script.

In this version, you can specify which brain regions to visualize, their transparency (alpha),
and colors via command-line arguments.
Example usage: Run this command in PowerShell (VS Code default):

python "C:/Users/David/OneDrive/Desktop/Python-assignments-main/day 02/Homework NeuroRender/HW_CLI_input.py" --regions MOs VISp --alpha 0.5 0.3 --colors salmon skyblue
"""

import argparse
from brainglobe_atlasapi import BrainGlobeAtlas
from brainrender import Scene

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(
        description="Display selected ARA regions in a 3D brain model using BrainRender."
    )
    parser.add_argument(
        "--regions",
        nargs="+",
        required=True,
        help="List of ARA region acronyms to render (e.g., MOs VISp ACA)."
    )
    parser.add_argument(
        "--alpha",
        nargs="+",
        type=float,
        default=None,
        help="Transparency values (must match the number of regions)."
    )
    parser.add_argument(
        "--colors",
        nargs="+",
        default=None,
        help="Colors for each region (must match the number of regions)."
    )

    args = parser.parse_args()

    # Load the atlas
    print(">> Loading atlas 'allen_mouse_25um' (first run may take a few minutes)...")
    atlas = BrainGlobeAtlas("allen_mouse_25um")
    print("Atlas loaded:", atlas.metadata["name"], "| resolution:", atlas.resolution)
    print("Number of structures:", len(atlas.structures))

    # Create a 3D scene
    scene = Scene(atlas_name="allen_mouse_25um")

    # Add selected brain regions
    num_regions = len(args.regions)
    for i, region in enumerate(args.regions):
        alpha = args.alpha[i] if args.alpha and i < len(args.alpha) else 0.5
        color = args.colors[i] if args.colors and i < len(args.colors) else None
        scene.add_brain_region(region, alpha=alpha, color=color)
        print(f"Added region {region} (alpha={alpha}, color={color})")

    print(">> Opening 3D window... (close it to exit)")
    scene.render()


if __name__ == "__main__":
    main()
