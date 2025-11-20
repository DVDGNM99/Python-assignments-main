@echo off
REM Activate env and run Tk GUI
call conda activate chem-reporter
python -m src.app_gui_tk

