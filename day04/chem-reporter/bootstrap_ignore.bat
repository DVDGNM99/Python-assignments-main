@echo off
:: bootstrap_chem_reporter.bat - Chem-Reporter project bootstrap (Windows / CMD-safe)
setlocal enabledelayedexpansion

REM --- destination dir (default: chem-reporter) ---
set "DEST_DIR=chem-reporter"
if not "%~1"=="" set "DEST_DIR=%~1"

echo [1/8] Creating folders in "%DEST_DIR%"...
mkdir "%DEST_DIR%" 2>nul
pushd "%DEST_DIR%"
mkdir assets src tests scripts results .github .github\workflows 2>nul

REM ======================================================================
REM Files
REM ======================================================================

echo [2/8] Writing .gitignore ...
> ".gitignore" (
  echo __pycache__/
  echo *.pyc
  echo *.pyo
  echo .DS_Store
  echo .env
  echo results/
  echo dist/
  echo build/
  echo *.egg-info/
  echo .rdkit_cache/
)

echo [3/8] Writing environment.yml ...
> "environment.yml" (
  echo name: chem-reporter
  echo channels:
  echo   - conda-forge
  echo dependencies:
  echo   - python=3.11
  echo   - rdkit
  echo   - pip
  echo   - pip:
  echo       - requests
  echo       - python-dotenv
  echo       - PySimpleGUI
  echo       - pytest
  echo       - pandas
)

echo [4/8] Writing README.md ...
> "README.md" (
  echo # Chem-Reporter
  echo.
  echo MVP per risoluzione SMILES ^-> metadati ^+ punto di fusione ^(PubChem^) e generazione output ^(SDF/JSON/CSV^).
  echo.
  echo ## Setup rapido
  echo \`\`\`bash
  echo conda env create -f environment.yml
  echo conda activate chem-reporter
  echo copy .env.example .env
  echo \`\`\`
  echo.
  echo ## Struttura
  echo - assets/
  echo - src/
  echo - tests/
  echo - scripts/
  echo - results/
)

echo [5/8] Writing .env.example ...
> ".env.example" (
  echo # Esempio variabili ambiente
  echo HTTP_TIMEOUT=20
  echo USER_AGENT=Chem-Reporter/0.1 ^(https://example.local^)
)

echo [6/8] Creating src package and placeholders ...
> "src\__init__.py" echo.
> "src\config.py" (
  echo from dataclasses import dataclass
  echo.
  echo @dataclass(frozen=True)
  echo class Settings:
  echo ^    http_timeout: int = 20
  echo ^    user_agent: str = "Chem-Reporter/0.1 (https://example.local)"
)
> "src\models.py" (
  echo from dataclasses import dataclass
  echo.
  echo @dataclass
  echo class Result:
  echo ^    input_smiles: str
)
> "src\rdkit_utils.py" echo # placeholder RDKIT utilities
> "src\pubchem.py" echo # placeholder PubChem wrapper
> "src\io_utils.py" echo # placeholder IO utilities

echo [7/8] Writing tests and scripts ...
> "tests\test_pubchem.py" echo def test_placeholder(): pass
> "scripts\run_app.bat" (
  echo @echo off
  echo python -m src.app_gui
)

echo [8/8] Writing CI workflow ...
> ".github\workflows\ci.yml" (
  echo name: CI
  echo on: [push]
  echo jobs:
  echo ^  test:
  echo ^    runs-on: windows-latest
  echo ^    steps:
  echo ^      - uses: actions/checkout@v4
  echo ^      - name: Setup conda
  echo ^        uses: conda-incubator/setup-miniconda@v3
  echo ^        with:
  echo ^          environment-file: environment.yml
  echo ^      - name: Run tests
  echo ^        run: pytest -q
)

REM --- Optional tiny icon (1x1 transparent PNG) ---
set "ICON_B64=assets\icon.b64"
> "%ICON_B64%" (
  echo iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQImWNgYGBgAAAABQABhZyQ8QAAAABJRU5ErkJggg==
)
certutil -f -decode "%ICON_B64%" "assets\icon.png" >nul 2>&1
del "%ICON_B64%" >nul 2>&1

popd

echo.
echo ✅ Struttura Chem-Reporter creata in: %CD%\%DEST_DIR%
echo    Prossimi passi:
echo      1^)^) cd "%DEST_DIR%"
echo      2^)^) conda env create -f environment.yml
echo      3^)^) conda activate chem-reporter
echo      4^)^) copy .env.example .env
echo.

endlocal
