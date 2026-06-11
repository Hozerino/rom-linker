@echo off
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('py2exe') or importlib.util.find_spec('PyInstaller') else 1)"
    if not errorlevel 1 (
        ".venv\Scripts\python.exe" setup.py
        if not errorlevel 1 goto done
    )
)

where py >nul 2>nul
if not errorlevel 1 (
    py -3.13 -c "import importlib.util, sys; sys.exit(0 if importlib.util.find_spec('py2exe') or importlib.util.find_spec('PyInstaller') else 1)"
    if not errorlevel 1 (
        py -3.13 setup.py
        if not errorlevel 1 goto done
    )
)

where python >nul 2>nul
if not errorlevel 1 (
    python setup.py
    if not errorlevel 1 goto done
)

echo.
echo Could not run Python. Install Python 3.13 from python.org or activate a working virtual environment.

:done
pause
