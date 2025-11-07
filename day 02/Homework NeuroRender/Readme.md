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
- Support three input modes (GUI, REPL, CLI) with consistent logic and output.  
- Provide an ARA region dropdown menu in the GUI for easier user interaction.  
- Cache downloaded data and store previously used regions in a JSON manifest.  
- Maintain a modular structure for future extensions (e.g., other species or atlases).  

---

## 2. Tech Stack and Dependencies

### Core Libraries
- **brainglobe-atlasapi** — load and query the Allen Mouse Brain Atlas.  
- **brainrender** — 3D visualization of brain regions.  
- **tkinter** — built-in GUI toolkit.  
- **argparse** — command-line argument parsing.  
- **numpy**, **pandas** — lightweight data processing.  
- **json** — manifest and cache management.

### Optional Libraries
- **pydantic** — schema validation for manifests.  
- **allensdk** — advanced querying from the Allen Brain Atlas.

---

## 3. Environment Setup

To prevent dependency conflicts between libraries (particularly different **numpy** versions required by `brainrender` and `allensdk`), the project uses **two separate virtual environments**:

- One environment, named **brainrender-env**, is dedicated to visualization and BrainGlobe tools.  
- A second environment, named **allensdk-env**, is used for data queries and analysis using the AllenSDK.  

Each script will be designed to automatically activate the correct environment before execution, ensuring stable compatibility and preventing version errors.

---

## 4. Directory Structure

All project files are contained within the directory:  
`C:\Users\David\OneDrive\Desktop\Python-assignments-main\day 02\Homework NeuroRender`

Inside that directory, the structure should be:

Homework NeuroRender/
  README.md
  requirements.txt
  data/
    cache/                     # BrainGlobe atlas cache
    manifests/
      areas_manifest.json      # stores requested regions and metadata
  src/
    core/
      atlas_io.py              # load atlas and retrieve ARA region names
      normalize.py             # normalize user input to ARA IDs
      visualize.py             # brainrender 3D plotting
    apps/
      gui_app.py               # GUI interface (dropdown + text input)
      repl_app.py              # interactive REPL interface
      cli_app.py               # command-line interface
    config.py                  # general configuration and environment setup
  tests/
    test_end_to_end.py


### Automatically Creating the Folder Structure (using miniforge prompt)

create the **entire project directory tree** described in section 4 using a few terminal commands.  
This ensures a clean, consistent layout before you start coding.


---

## 5. GUI Design

The GUI (built with `tkinter`) provides:  
- A dropdown menu populated with all ARA region names.  
- Manual input for additional regions.  
- Buttons for:
  - **Render** — visualize the selected regions.  
  - **Clear** — reset input and selections.  
- A small status area showing region IDs, errors, or logs.

---

## 6. Manifest and Caching

### Manifest
The file `data/manifests/areas_manifest.json` keeps track of all previously visualized brain regions and related metadata.

### Caching
Downloaded atlas data are stored locally in `data/cache/` for faster access during subsequent runs.

---

## 7. Automation and Environment Switching

Each main script (GUI, CLI, and REPL) will automatically activate the appropriate virtual environment before running the main logic.  
This ensures compatibility with the required dependencies and isolates visualization code from data-querying modules.

---
All three interfaces (GUI, REPL, CLI) rely on the same backend, ensuring identical results.