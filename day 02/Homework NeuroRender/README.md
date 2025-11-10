# BrainGlobe Render Environment
---
## Example images
![imagine](https://github.com/DVDGNM99/Python-assignments-main/blob/main/Screenshot%202025-11-07%20173958.png)
![imagine](https://github.com/DVDGNM99/Python-assignments-main/blob/main/Screenshot%202025-11-07%20174726.png)
---
## Environment name
`brainglobe_render`
---
This environment is dedicated to **3D visualization and anatomical analysis of the mouse brain** using the **BrainGlobe ecosystem**.  
---
## Installation, Create an environment:
- Download Anaconda/ Miniforge/ Miniconda/ Mamba (one of them is enough)
- Create the environment:
### list of commands to create an env (copy in the prompt of conda)
1. conda config --add channels conda-forge
2. conda config --set channel_priority strict
3. conda create -n brainglobe_render -y -c conda-forge ^
  python=3.10 numpy pandas scipy pyqt "vtk<9.5.2" vedo pyvista k3d pytables ^
  brainglobe-atlasapi brainglobe-space brainglobe-utils
4. conda activate brainglobe_render
5. pip install morphapi brainrender==2.1.16
6. conda env list
python -c "import brainrender, morphapi; print('OK: brainrender e morphapi importati')"
python -m pip list | findstr brainrender
- ( N. 6 is just a test. it will print out all your environments and you should be able to see one called brainglobe_render )
---
## Core dependencies
look at the environment.yml file inside the folder
- all the dependencies should be in the environment created following the steps in "list of commands"
---
## Maintenance and updates
1. Conda activate brainglobe_render
2. Conda update -c conda-forge vtk vedo pyqt brainglobe-atlasapi -y
3. pip install --upgrade brainrender morphapi brainglobe-utils
- Note: Avoid upgrading vtk beyond version 9.5.1, since newer builds may cause incompatibilities with brainrender.
---
## Important for future self
- this env can later be extended to include the full BrainGlobe suite (cellfinder, brainreg, etc.) if required for volumetric analysis.
- regions.json file includes all the brain areas in the ARA dictionary. not all of them will work with biorender. I suggest trying with some standard areas such as: MOs, VISp, ACA, TH, APN.
  in alternative rename the file regions_partial.json in regions.json to have a simplified list in the GUI
---
## Tools
  - Chatgpt version 5 was used to troubleshoot and for the creation on the enviroment
  
  
