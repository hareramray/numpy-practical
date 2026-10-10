@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo The local Python environment is missing. Follow the setup steps in README.md.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" -m jupyterlab notebooks/00_start_here.ipynb
if errorlevel 1 pause
