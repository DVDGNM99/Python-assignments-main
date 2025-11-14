# Neurorender Logic Update – day03
for additional informations and explanation [click here](https://github.com/DVDGNM99/Python-assignments-main/blob/main/day02/Homework%20NeuroRender/README.md)
---
**Objective**:

This project refactors the day02 GUI script by separating the business logic (region loading, validation, color management) from rendering and the user interface.
This makes the code:

- Testable without opening the GUI

- More robust and maintainable

- Easier to extend

---
# Project structure:
```text

Neurorender_Logic_update/
├── .pytest_cache/
├── App/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── cli.py            → command-line entrypoint
│   ├── gui.py            → lightweight Tkinter GUI orchestrating logic.py and rendering.py
│   ├── logic.py          → pure functions: JSON parsing, region deduplication, acronym validation, color normalization, input preparation for renderer
│   └── rendering.py      → wrapper for brainglobe_atlasapi/brainrender (load atlas, build scene, add regions, render)
├── tests/
│   ├── __pycache__/
│   ├── conftest.py       → pytest configuration and fixtures
│   ├── test_logic.py     → unit tests for logic.py
│   └── test_rendering.py → unit tests for rendering.py
├── .coverage
├── environment.yml       → Conda environment file
├── HW_GUI_input.py       → original day02 script (for reference)
├── README.md
└── regions.json          → Brain regions file

```
---
# Changes from the Original Script
The project has been completely refactored to separate computation, visualization, and interface code, making it cleaner, easier to maintain, and testable.

## **Role Separation**:
The original script mixed graphical interface code (Tkinter) with all the logic for reading the JSON file, checking acronyms, and rendering the brain model.
Now, each part has a clear responsibility:

- App/logic.py handles all pure computations such as reading JSON data, removing duplicates, validating acronyms, and managing colors. These functions do not depend on the GUI and can be tested independently.

- App/rendering.py contains the interface with brainrender and brainglobe_atlasapi. It loads the atlas, creates the 3D scene, and adds regions to it.

- App/gui.py only controls the user interface and calls the functions from logic and rendering. This keeps the GUI lightweight and stable.
This separation makes debugging easier and allows each component to evolve without breaking the others.

## **Validation and Robustness**
The new code includes strong input validation and clearer error handling:

- Alpha transparency must be between 0 and 1.

- Colors are validated to ensure they follow the #RRGGBB format.

- Region acronyms are extracted safely from labels like “ACR — Region name”.

- Errors from invalid JSON files or atlas loading are caught and reported with clear, specific messages.
These checks make the program more reliable and protect it from user mistakes or corrupted files.

## **Improved Pre-render Preparation**
The “Load & Prepare” step was redesigned. It now:

- Parses the JSON file and lists all regions.

- Loads the atlas only to collect available structures (faster than rendering everything).

- Compares the JSON data with the atlas and separates valid from invalid regions.

- Only valid regions are rendered, and the user is informed about any invalid ones.
This approach avoids crashes and makes rendering more predictable.

## **Testability**
All logic can now be tested without opening the GUI or downloading an atlas.

- tests/test_logic.py verifies JSON parsing, data normalization, and input validation.

- tests/test_rendering.py mocks the 3D scene to check that region addition works correctly.
This ensures correctness while keeping tests fast and independent of external libraries.

Overall, the refactor transforms the original script into a modular, maintainable, and professional tool.
---
# Software requirements

To run the project smoothly, make sure your system meets the following conditions:

- Conda must be installed with the conda-forge channel enabled, since most scientific and visualization packages come from that source.

- An internet connection is required the first time you launch the program, as brainglobe will automatically download the selected brain atlas.

- A system with proper OpenGL support (or a compatible GPU) is needed for brainrender to display the 3D scene correctly.
---
# Installation

1. Open a terminal and navigate to the project folder containing the environment.yml file.

2. Create the Conda environment that includes all required libraries:
conda env create -f environment.yml

3. Activate the environment before running any part of the project:
conda activate brainglobe_render
** for more info [click here](https://github.com/DVDGNM99/Python-assignments-main/tree/main/day02/Homework%20NeuroRender#installation-create-an-environment).** 
Once the environment is active, all commands (GUI, CLI, and tests) will have access to the necessary dependencies.
---
# Running the GUI

1. Open a terminal and move to the project root folder (Neurorender_logic_update).

2. Start the graphical interface with:
python -m App.gui

3. When the window opens:

- Confirm or browse to your regions.json file.

- Choose the desired atlas (default: allen_mouse_25um).

- Set the alpha transparency value between 0 and 1.

- Click “Load & Prepare” to parse the JSON, load the atlas, and check which regions are valid.

- Click “Render” to open the 3D brain visualization with the selected regions.
---
# Running the CLI
The program can also be used entirely from the command line for quick checks or headless runs.

To validate a JSON file of regions against a given atlas:
python -m App.cli validate-json regions.json --atlas allen_mouse_25um

This prints how many regions are valid and how many are not recognized in the atlas.

To render specific regions directly (without opening the Tkinter interface):
python -m App.cli render-regions MOs,VISp,ACA --atlas allen_mouse_25um --alpha 0.5

This command launches brainrender, builds the scene, and displays only the listed regions using the given transparency value.

The CLI is ideal for automation, quick testing, or running on systems without a desktop environment.
---
# Running Tests
```
├── tests/
│   ├── test_logic.py       → tests pure functions
│   ├── test_rendering.py   → mocks rendering to verify region addition calls
│   └── conftest.py         → ensures App package is importable
```
**All tests are located in the tests folder and are designed to check the project’s logic and structure without depending on the GUI or a real 3D render.**
- To execute all tests, open a terminal in the project root and run:
```bash
pytest -q
```
To see code coverage as well:
```bash
pytest --cov=App
```
If pytest reports that it cannot find the App module, verify that the tests folder contains a file named conftest.py with the following content:
```py
import sys, pathlib
ROOT = pathlib.Path(file).resolve().parents[1]
if str(ROOT) not in sys.path:
sys.path.insert(0, str(ROOT))
```
---
# Operational Notes

- The first time you load an atlas, the system will download the dataset; future runs are faster because the atlas is cached locally.

- If the GUI opens but does not render the 3D model, check your graphics driver and OpenGL or Vulkan compatibility.

- Both the GUI and CLI rely on the same logic modules, so they will remain synchronized as new features are added.

- Typer and Rich are already included, making it easy to expand the CLI with more commands in the future.

---
# Third-Party Libraries Used

- brainrender (3D rendering)
- brainglobe-atlasapi (atlas access)
- morphapi (morphology integration)
- typer (CLI)
- rich (CLI formatting)
- pytest, pytest-cov (testing)
- numpy, pandas, pyvista, vedo (numerical and visualization stack)
