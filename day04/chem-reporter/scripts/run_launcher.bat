@echo on
REM --- Find conda.bat robustly ---
set "CONDA_BAT="
for %%F in ("%USERPROFILE%\miniforge3\condabin\conda.bat" ^
            "%USERPROFILE%\mambaforge\condabin\conda.bat" ^
            "C:\ProgramData\miniforge3\condabin\conda.bat") do (
  if exist "%%~F" set "CONDA_BAT=%%~F"
)
if not defined CONDA_BAT (
  for /f "delims=" %%P in ('where conda.bat 2^>nul') do set "CONDA_BAT=%%P"
)
if not defined CONDA_BAT (
  echo Could not find conda.bat && pause && exit /b 1
)
call "%CONDA_BAT%" activate chem-reporter

cd /d "C:\Python-assignments-main\day04\chem-reporter"
set PYTHONUTF8=1
python -u -m src.launcher_gui
if exist "%CD%\results" start "" "%CD%\results"
pause
