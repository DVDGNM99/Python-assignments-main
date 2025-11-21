@echo on
call "C:\Users\David\miniforge3\condabin\conda.bat" activate chem-reporter
cd /d "C:\Python-assignments-main\day04\chem-reporter"
set PYTHONUTF8=1
python -u -m src.launcher_gui
if exist "%CD%\results" start "" "%CD%\results"
pause
