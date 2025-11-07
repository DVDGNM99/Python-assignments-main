# make an interesting program using some inspiration from our labs and use the 3 input ways we have seen in class
## i decided to make a visualization tool for brain regions in the mouse using Allen/ Brainglobe atlases
---
The project will provide three separate runnable files that all display identical results for the same inputs:

1. GUI app — includes text boxes and a dropdown menu with ARA region names.

2. REPL app — uses Python’s built-in input() prompts.

3. CLI app — uses command-line arguments.
---
## 1. Project Goals

- Query and visualize brain regions from the **Allen Mouse Brain Atlas** via **BrainGlobe**.  
- Allow three different input modes (GUI, REPL, CLI) with consistent outputs.  
- Provide an **ARA region dropdown menu** in the GUI for easy selection.  
- Cache downloaded data and track used regions in a local JSON manifest.  
- Keep the design modular for future extensions (e.g., new species or atlases).

---

## 2. Tech Stack and Dependencies

**Core libraries**
- `brainglobe-atlasapi` — load/query Allen Mouse Brain Atlas data.  
- `brainrender` — visualize 3D brain regions.  
- `tkinter` — GUI toolkit (bundled with Python).  
- `argparse` — for CLI argument parsing.  
- `numpy`, `pandas` — light data processing.  
- `json` — for the manifest.

**Optional**
- `pydantic` — for manifest schema validation.  
- `allensdk` — for more advanced queries from the Allen Brain Atlas.

---

## 3. Environment Setup

(Bash)
1. Create and activate an environment
mamba create -n mouse-brain python=3.11 -y
mamba activate mouse-brain

2. Install dependencies
pip install brainglobe-atlasapi brainrender numpy pandas
pip install allensdk pydantic

---

## 4. Environment Setup

mouse-brain-areas-viewer/
├─ README.md
├─ requirements.txt
├─ data/
│  ├─ cache/                     # BrainGlobe atlas cache
│  └─ manifests/
│     └─ areas_manifest.json     # stores previously requested regions
├─ src/
│  ├─ core/
│  │  ├─ atlas_io.py             # load atlas, get ARA region names
│  │  ├─ normalize.py            # normalize user text to ARA IDs
│  │  └─ visualize.py            # brainrender 3D plotting
│  ├─ apps/
│  │  ├─ gui_app.py              # GUI (with dropdown + text input)
│  │  ├─ repl_app.py             # REPL (input())
│  │  └─ cli_app.py              # CLI (argparse)
│  └─ config.py                  # configuration (atlas, paths, cache)
└─ tests/
   └─ test_end_to_end.py

### Automatically Creating the Folder Structure (using miniforge prompt)

You can quickly create the **entire project directory tree** described in section 4 using a few terminal commands.  
This ensures a clean, consistent layout before you start coding.


---

## 5. The ARA Region Dropdown (GUI)

Data Source:

## The Allen Reference Atlas (ARA) provides hierarchical brain region names like:

- Primary visual area (VISp)

- Primary motor area (MOp)

- Hippocampal region (HIP)

load them directly from BrainGlobe-> 

### GUI Design

A dropdown menu (tkinter.OptionMenu or Combobox) lists all ARA region names.

- Users can:

1. Select one or more regions from the dropdown.

2. Type region names manually in a text box.

- Buttons:

1. Render → visualize the selected regions.

2. Clear → reset selection.

3. A small status panel displays selected region IDs and any errors.
---
## 6. Manifest and Caching

### Manifest File
`data/manifests/areas_manifest.json` keeps track of all previously requested brain regions, their usage, and metadata.  
---
All three interfaces (GUI, REPL, CLI) rely on the same backend, ensuring identical results.