@echo off
setlocal enabledelayedexpansion

REM Go to project root (this .bat is inside scripts\)
pushd "%~dp0\.."

REM --- Robust Conda activation on Windows ---
if exist "%USERPROFILE%\miniconda3\condabin\conda.bat" (
  call "%USERPROFILE%\miniconda3\condabin\conda.bat" activate chem-reporter
) else if exist "%USERPROFILE%\miniforge3\condabin\conda.bat" (
  call "%USERPROFILE%\miniforge3\condabin\conda.bat" activate chem-reporter
) else (
  where conda >nul 2>&1
  if %errorlevel%==0 (
    call conda activate chem-reporter
  ) else (
    echo Could not find Conda.
    echo Open "Anaconda Prompt" and run:
    echo     conda activate chem-reporter ^&^& python -m src.app_gui
    pause
    exit /b 1
  )
)

echo Launching Chem-Reporter GUI...
python -m src.app_gui
set rc=%errorlevel%

popd
echo.
if %rc% neq 0 (
  echo Python exited with code %rc%.
)
pause
endlocal
