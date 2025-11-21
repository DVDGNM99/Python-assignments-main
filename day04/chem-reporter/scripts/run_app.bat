@echo on
REM === Activate your conda env ===
call "C:\Users\David\miniforge3\condabin\conda.bat" activate chem-reporter

REM === Go to project root ===
cd /d "C:\Python-assignments-main\day04\chem-reporter"

REM === Launch Tkinter app (show tracebacks) ===
set PYTHONUTF8=1
python -X dev -u -m src.app_gui
echo Exit code: %ERRORLEVEL%

pause
