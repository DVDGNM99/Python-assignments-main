@echo off
setlocal
if "%~1"=="" (
  echo Usage: run_batch.bat path\to\input.csv
  exit /b 1
)
call conda activate chem-reporter
python scripts\run_batch.py "%~1" --results results
endlocal
