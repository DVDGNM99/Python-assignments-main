# Neurorender Logic Update – day03
---
Objective

This project refactors the day02 GUI script by separating the business logic (region loading, validation, color management) from rendering and the user interface.
This makes the code:

Testable without opening the GUI

More robust and maintainable

Easier to extend
---
# Project structure:
Neurorender_logic_update/
├── App/
│   ├── __init__.py
│   ├── logic.py        → pure functions: JSON parsing, region deduplication, acronym validation, color normalization, input preparation for renderer
│   ├── rendering.py    → thin wrapper for brainglobe_atlasapi and brainrender (load atlas, build scene, add regions, render)
│   └── gui.py          → lightweight Tkinter GUI orchestrating logic.py and rendering.py
│
├── tests/
│   └── test_logic.py   → unit tests for pure functions in logic.py (no GUI, no atlas download)
│
├── HW_GUI_input.py     → original day02 script (for reference)
├── regions.json        → example region file
├── environment.yml     → updated conda environment
└── README.md           → this file
---
# Changes from the Original Script
Role Separation

Parsing and validation functions moved to App/logic.py (no GUI calls inside).

Direct calls to brainrender and atlas isolated in App/rendering.py.

The GUI now only calls logic and rendering functions, simplifying the interface code.

Validation and Robustness

Alpha validation: must be between 0 and 1.

Color validation: accepts only #RRGGBB format.

Acronym parsing: robust extraction from strings like ACR — Name.

Error handling: clear distinction between JSON errors and atlas-loading issues (dedicated exceptions).

Pre-render Preparation

The “Load & Prepare” step:

Parses JSON

Loads atlas only to retrieve the list of structures

Splits regions into valid and invalid

Rendering uses only validated regions; invalid ones are reported to the user.

Testability

tests/test_logic.py covers:

JSON parsing

Normalization of selections and colors

Input validation

No GUI or atlas download is required.
---
# Software requirements

Conda with the conda-forge channel enabled

Internet connection on the first run (to download the atlas via brainglobe)

System with OpenGL support (required by brainrender for 3D visualization)
---
# Installation

Create the environment:

conda env create -f environment.yml


Activate it:

conda activate brainglobe_render
---
# Running the GUI

Navigate to the project root (Neurorender_logic_update/):

python -m App.gui

In the GUI

Select or confirm the path to regions.json

Set the atlas (default: allen_mouse_25um)

Set alpha between 0 and 1

Click Load & Prepare to validate regions against the atlas

Click Render to visualize the 3D scene
---
# Running the CLI
You can use a command-line interface instead of the GUI.

Validate a JSON file:
python -m App.cli validate-json regions.json --atlas allen_mouse_25um

Render specific regions directly:
python -m App.cli render-regions MOs,VISp,ACA --atlas allen_mouse_25um --alpha 0.5
---
# Running Tests
├── tests/
│   ├── test_logic.py       → tests pure functions
│   ├── test_rendering.py   → mocks rendering to verify region addition calls
│   └── conftest.py         → ensures App package is importable

From the project root:

pytest -q


(Optional, with coverage):

pytest --cov=App

If pytest cannot find the App module, make sure a file named conftest.py exists in the tests folder containing:

import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

---
# Operational Notes

The first atlas load may take some time (downloads data); subsequent runs are faster.

If the GUI window remains blank or does not render, check:

Graphics drivers

OpenGL/Vulkan compatibility

CLI support is planned — typer and rich are already included for future expansion.
If pytest and the GUI both run successfully, open an issue on the course repository titled:
day03 <Your Name> – including the link to your day03 folder and the two peer issues you opened.

---
# Third-Party Libraries Used

- brainrender (3D rendering)
- brainglobe-atlasapi (atlas access)
- morphapi (morphology integration)
- typer (CLI)
- rich (CLI formatting)
- pytest, pytest-cov (testing)
- numpy, pandas, pyvista, vedo (numerical and visualization stack)
