"""
Command Line Interface (CLI) for NeuroRender
--------------------------------------------
This provides quick, non-GUI commands to validate region JSONs and render
specific regions directly from the terminal.

Usage examples:
    python -m App.cli validate-json regions.json --atlas allen_mouse_25um
    python -m App.cli render-regions MOs,VISp,ACA --atlas allen_mouse_25um --alpha 0.5
"""

from __future__ import annotations
import json
from pathlib import Path
import typer
from rich.console import Console

from App.logic import (
    load_regions_from_json,
    prepare_render_inputs,
    validate_acronyms,
)
from App.rendering import (
    load_atlas,
    get_structures,
    build_scene,
    add_regions,
    render,
    AtlasLoadError,
)

console = Console()
app = typer.Typer(help="Headless utilities for NeuroRender")

# ------------------------------------------------------------ #
# validate-json
# ------------------------------------------------------------ #
@app.command("validate-json")
def validate_json(
    json_path: Path = typer.Argument(..., help="Path to a regions.json file"),
    atlas: str = typer.Option("allen_mouse_25um", help="Atlas name to validate against"),
):
    """Validate a JSON file of regions against the selected atlas."""
    try:
        items = load_regions_from_json(json_path)
        displays = [i.display for i in items]
        atlas_obj = load_atlas(atlas)
        structs = get_structures(atlas_obj)
        acrs, _, _ = prepare_render_inputs(displays, None, 0.5)
        valid, invalid = validate_acronyms(acrs, structs)
        console.print(f"[green]Valid regions:[/green] {len(valid)}")
        console.print(f"[red]Invalid regions:[/red] {len(invalid)}")
        if invalid:
            console.print(", ".join(invalid[:20]) + ("..." if len(invalid) > 20 else ""))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

# ------------------------------------------------------------ #
# render-regions
# ------------------------------------------------------------ #
@app.command("render-regions")
def render_regions(
    regions_csv: str = typer.Argument(..., help="Comma-separated list of region acronyms (e.g. MOs,VISp,ACA)"),
    atlas: str = typer.Option("allen_mouse_25um", help="Atlas name to use"),
    alpha: float = typer.Option(0.5, help="Transparency level between 0 and 1"),
):
    """Render one or more brain regions directly without opening the Tkinter GUI."""
    try:
        acrs = [a.strip() for a in regions_csv.split(",") if a.strip()]
        from App.logic import cycle_colors
        colors = cycle_colors(len(acrs))
        scene = build_scene(atlas)
        add_regions(scene, acrs, colors, alpha)
        console.print(f"[cyan]Rendering {len(acrs)} region(s) from {atlas}...[/cyan]")
        render(scene)
    except AtlasLoadError as e:
        console.print(f"[bold red]Atlas error:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]Render error:[/bold red] {e}")

# ------------------------------------------------------------ #

if __name__ == "__main__":
    app()
