@echo on
setlocal
REM === Project root is the parent of /scripts ===
set "PROJECT_ROOT=%~dp0.."

REM === Activate Conda env (adjust path if your Miniforge is elsewhere) ===
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


cd /d "%PROJECT_ROOT%"
set PYTHONUTF8=1

REM === Manual mode UI/CLI entrypoint ===
python -u -m src.app_gui

set "CODE=%ERRORLEVEL%"
if exist "%PROJECT_ROOT%\results" start "" "%PROJECT_ROOT%\results"
echo Exit code: %CODE%
endlocal
pause
