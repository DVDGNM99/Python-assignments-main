# Chem-Reporter (MVP)

Windows-ready chemistry utility for resolving SMILES via PubChem and extracting melting points (°C). with a feature to visualize molecules
---
### 2D

- ![imagine](https://github.com/DVDGNM99/Python-assignments-main/blob/main/Images/2D.png)
---
### 3D interactive

- ![imagine](https://github.com/DVDGNM99/Python-assignments-main/blob/main/Images/3D.png)

---
## Quick start (one click)

Recommended for new users (even without Python/Conda installed):

1. Download/clone this folder from GitHub.

2. Double-click: bootstrap_chem_reporter.bat

```txt
What the bootstrap does:

Detects (or installs) Miniforge in your user profile (no admin needed).

Creates/updates the chem-reporter conda environment from environment.yml.

Ensures the launcher works and creates a Desktop shortcut (supports OneDrive Desktop).

Starts the Unified Launcher GUI.

If Windows warns about execution policy, right-click the .bat → Run anyway.
The Desktop link will appear under your real Desktop path (often C:\Users\<you>\OneDrive\Desktop).
```

## ⚙️ Setup

Requires:
- Miniforge / Conda
- Windows 10 or 11
- Internet connection (for live PubChem)

Create the environment:
```bash
conda env create -f environment.yml
conda activate chem-reporter
copy .env.example .env
```
## 🚀 Usage
### single compound (paste in the window and example molecule:CC(=O)OC1=CC=CC=C1C(=O)O)
```bash
scripts\run_app.bat
```
### Batch (CSV list), example inside input folder
```bash
scripts\run_batch.bat input\test_molecules.csv
```
### Unified launcher GUI
```bash
scripts\run_launcher.bat
```
---
## GUI launcher
- choose option manually or fetch CSV

-![imagine](https://github.com/DVDGNM99/Python-assignments-main/blob/main/Images/chem_GUI_1.png)
---
## Manual
- paste a SMILES structure in the box and press search
- example SMILES: aspirin: CC(=O)OC1=CC=CC=C1C(=O)O 

-![imagine](https://github.com/DVDGNM99/Python-assignments-main/blob/main/Images/chem_GUI_insertmanual.png)
---
## Fetch a CSV 
- in the folder: input you can find an example csv

-![imagine](https://github.com/DVDGNM99/Python-assignments-main/blob/main/Images/chem_GUI_csv.png)
---

## 🧩 Output structure
Each compound folder includes:
```txt
results/<compound>/
  metadata.json
  melting_point.csv
  structure.sdf
  IUPAC.txt
```
---
## Using structure.sdf from the output visualize your molecules
- open ```visualize_molecule.ipynb``` and run the cells
---
### 2D molecule 

- ![imagine](https://github.com/DVDGNM99/Python-assignments-main/blob/main/Images/2D.png)
---
### 3D molecule

- ![imagine](https://github.com/DVDGNM99/Python-assignments-main/blob/main/Images/3D.png)
---
A global summary.csv aggregates all results.
## 🧪 Offline tests
Offline unit tests use cached PubChem JSONs (aspirin/caffeine) to verify parsing.
```bash
pytest
```
## Project structure
```text
chem-reporter/
  assets/
    icon.ico
  input/
    test_molecules.csv
  results/                   # auto-created by runs
  scripts/
    run_app.bat
    run_batch.bat
    run_launcher.bat
    run_batch.py
  src/
    app_gui.py               # GUI for single compound
    launcher_gui.py          # Unified launcher (Tkinter)
    pubchem.py               # network + parsing
    io_utils.py, rdkit_utils.py, models.py, config.py
  tests/
    data/                    # cached JSON (aspirin/caffeine)
    test_offline_parsing.py
  tools/
    make_shortcut.ps1
  environment.yml
  bootstrap_chem_reporter.bat
  README.md
```
## Configuration
edit ```src/config.py```
- ```TIMEOUT_SECONDS``` – HTTP timeout for PubChem requests
- ```USER_AGENT``` – sent with every request (keep it informative)
logging is enabled in entrypoints>
```python
import logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
```
## Troubleshooting
- No Desktop shortcut appears: Your Desktop may be under OneDrive. The bootstrap targets the real path from
- PowerShell: [Environment]::GetFolderPath('Desktop'). Check that folder.
- “No module named src” running tests: Ensure tests/conftest.py exists and src/__init__.py is present.
- Icon not showing in taskbar: Tkinter sets the window icon; the taskbar may still show python.exe until packaging (post-MVP).

Conda not found: The bootstrap auto-installs Miniforge. If you prefer manual install, install Miniforge and re-run.
## 📦 Packaging
To make a portable version:

1. Zip the project folder with /scripts/*.bat and /assets/icon.ico

2. Optionally create a desktop shortcut via PowerShell script in tools/make_shortcut.ps1
