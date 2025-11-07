# BrainGlobe Render Environment

![imagine](https://github.com/DVDGNM99/Python-assignments-main/blob/main/Screenshot%202025-11-07%20173958.png)
![imagine](https://github.com/DVDGNM99/Python-assignments-main/blob/main/Screenshot%202025-11-07%20174726.png)
## Environment name
`brainglobe_render`

This environment is dedicated to **3D visualization and anatomical analysis of the mouse brain** using the **BrainGlobe ecosystem**.  
It is configured as a lightweight, stable environment that focuses on rendering and atlas access, keeping heavy dependencies separated from other analysis environments.

---

## Core dependencies

| Package | Version | Purpose |
|----------|----------|----------|
| **python** | 3.10.x | compatible version for VTK and BrainGlobe stack |
| **brainrender** | 2.1.x | 3D visualization and rendering of brain structures |
| **brainglobe-atlasapi** | 2.3.x | access and management of reference brain atlases (e.g., Allen Mouse Atlas) |
| **brainglobe-space** | – | coordinate systems and spatial transformations |
| **brainglobe-utils** | – | shared utilities within the BrainGlobe ecosystem |
| **morphapi** | – | download and render neuron morphologies (e.g., NeuroMorpho) |
| **pyvista** | 0.46.x | 3D visualization backend for brainrender |
| **vedo** | 2025.x | rendering library built on VTK |
| **vtk** | < 9.5.2 | scientific visualization engine |
| **pyqt** | 5.x | graphical interface backend for rendering windows |
| **k3d** | – | optional interactive visualization support for Jupyter notebooks |
| **pytables** | – | HDF5 data management (required by brainrender) |
| **numpy**, **pandas**, **scipy** | – | general scientific and numerical support |

---

## Installation

Create the environment from scratch (using Miniforge or Mambaforge):

### use file: enviroment.yml 
- (bash)
mamba env create -f environment.yml


## Maintenance and updates
1. mamba activate brainglobe_render
2. mamba update -c conda-forge vtk vedo pyqt brainglobe-atlasapi -y
3. pip install --upgrade brainrender morphapi brainglobe-utils
- Avoid upgrading vtk beyond version 9.5.1, since newer builds may cause incompatibilities with brainrender.

# Important for future self
- this env can later be extended to include the full BrainGlobe suite (cellfinder, brainreg, etc.) if required for volumetric analysis.

- All dependencies are sourced from conda-forge for maximum compatibility and stability.
- regions.json file includes all the brain areas in the ARA dictionary. not all of them will work with biorender. I suggest trying with some standard areas such as: MOs, VISp, ACA, TH, APN.
  in alternative rename the file regions_partial.json in regions.json to have a simplified list in the GUI

  ## Tools
  - Chatgpt version 5 was used to troubleshoot and for the creation on the enviroment
  
  
