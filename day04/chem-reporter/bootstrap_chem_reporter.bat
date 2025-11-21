@echo off
setlocal ENABLEDELAYEDEXPANSION

REM ============================================================
REM  Chem-Reporter bootstrap (Windows, user scope)
REM  - Installs Miniforge if missing (no admin needed)
REM  - Creates/updates conda env from environment.yml
REM  - Builds icon (png -> ico) if needed
REM  - Creates Desktop shortcut to run_launcher.bat
REM  - Launches the unified launcher GUI
REM ============================================================

REM --- Project root is the folder of this .bat ---
set "PROJECT_ROOT=%~dp0"
REM trim trailing backslash if any
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

echo.
echo [1/6] Detecting conda/miniforge...
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
  echo - Miniforge not found. Downloading and installing in "%USERPROFILE%\miniforge3" ...
  set "MINI_URL=https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe"
  set "MINI_EXE=%TEMP%\miniforge3-installer.exe"
  powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest '%MINI_URL%' -OutFile '%MINI_EXE%'" || (
    echo ERROR: failed to download Miniforge installer. Check your internet connection.
    pause & exit /b 1
  )
  start /wait "" "%MINI_EXE%" /S /D=%USERPROFILE%\miniforge3
  del /q "%MINI_EXE%" 2>nul
  set "CONDA_BAT=%USERPROFILE%\miniforge3\condabin\conda.bat"
)

if not exist "%CONDA_BAT%" (
  echo ERROR: conda.bat not found at "%CONDA_BAT%".
  pause & exit /b 1
)

echo.
echo [2/6] Creating/updating conda environment "chem-reporter"...
call "%CONDA_BAT%" activate base

REM Does env exist?
set "ENV_EXISTS="
for /f "tokens=1" %%E in ('conda env list ^| findstr /r /c:"^chem-reporter"') do set "ENV_EXISTS=yes"

if not defined ENV_EXISTS (
  echo - Env not found. Creating from environment.yml ...
  call conda env create -f "%PROJECT_ROOT%\environment.yml" -n chem-reporter || (
    echo ERROR: failed to create environment from environment.yml
    pause & exit /b 1
  )
) else (
  echo - Env exists. Updating from environment.yml ...
  call conda env update  -f "%PROJECT_ROOT%\environment.yml" -n chem-reporter
)

echo.
echo [3/6] Activating env and ensuring Pillow/dotenv/pytest present...
call "%CONDA_BAT%" activate chem-reporter
REM (optional safety) ensure these are present even if missing from YAML
python - <<EOF
import sys, subprocess
def ensure(pkg): subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
# comment these lines out if you strictly want conda-only
# ensure("pillow"); ensure("python-dotenv"); ensure("pytest")
print("Python:", sys.version)
EOF

echo.
echo [4/6] Building icon if needed...
if not exist "%PROJECT_ROOT%\assets\icon.ico" (
  if exist "%PROJECT_ROOT%\assets\icon.png" (
    python - <<EOF
from PIL import Image, ImageOps
from pathlib import Path
p = Path(r"%PROJECT_ROOT%\assets\icon.png")
ico = p.with_suffix(".ico")
img = Image.open(p).convert("RGBA")
# optional: pad to square
s = max(img.size); canvas = Image.new("RGBA",(s,s),(0,0,0,0)); canvas.paste(img,((s-img.width)//2,(s-img.height)//2))
canvas.save(ico, sizes=[(256,256),(128,128),(64,64),(32,32),(16,16)])
print("Built", ico)
EOF
  ) else (
    echo - No icon.png found; skipping ICO generation.
  )
) else (
  echo - icon.ico already present.
)

echo.
echo [5/6] Creating Desktop shortcut (handles OneDrive)...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ProjectRoot='%PROJECT_ROOT%';" ^
  "$TargetBat=Join-Path $ProjectRoot 'scripts\run_launcher.bat';" ^
  "$IconPath =Join-Path $ProjectRoot 'assets\icon.ico';" ^
  "$Desktop=[Environment]::GetFolderPath('Desktop');" ^
  "$Shortcut=Join-Path $Desktop 'Chem-Reporter.lnk';" ^
  "$W=New-Object -ComObject WScript.Shell; $L=$W.CreateShortcut($Shortcut);" ^
  "$L.TargetPath=$TargetBat; $L.WorkingDirectory=$ProjectRoot; $L.IconLocation=(Test-Path $IconPath)?$IconPath:$TargetBat; $L.WindowStyle=1; $L.Save();" ^
  "Write-Host ('Shortcut -> ' + $Shortcut)"

echo.
echo [6/6] Launching unified GUI...
call "%CONDA_BAT%" activate chem-reporter
cd /d "%PROJECT_ROOT%"
python -u -m src.launcher_gui

echo.
echo Done.
pause
