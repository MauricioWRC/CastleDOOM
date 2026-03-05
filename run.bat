@echo off
setlocal EnableExtensions

rem Always run from this .bat file's folder
cd /d "%~dp0"

set "VENV_DIR=.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"

echo [1/3] Checking virtual environment...
if not exist "%VENV_PY%" (
    echo .venv not found. Creating...
    py -3 -m venv "%VENV_DIR%" >nul 2>&1
    if errorlevel 1 (
        python -m venv "%VENV_DIR%"
        if errorlevel 1 (
            echo Failed to create virtual environment.
            exit /b 1
        )
    )
) else (
    echo .venv already exists.
)

echo [2/3] Checking requirements in .venv...
set "NEED_INSTALL="
"%VENV_PY%" -m pip show packaging >nul 2>&1 || set "NEED_INSTALL=1"
"%VENV_PY%" -m pip show pygame-ce >nul 2>&1 || set "NEED_INSTALL=1"
"%VENV_PY%" -m pip show setuptools >nul 2>&1 || set "NEED_INSTALL=1"
"%VENV_PY%" -m pip show wheel >nul 2>&1 || set "NEED_INSTALL=1"

if defined NEED_INSTALL (
    echo Missing dependencies. Installing from requirements.txt...
    if not exist "requirements.txt" (
        echo requirements.txt not found.
        exit /b 1
    )
    "%VENV_PY%" -m pip install --upgrade pip
    if errorlevel 1 exit /b 1

    "%VENV_PY%" -m pip install -r requirements.txt
    if errorlevel 1 exit /b 1
) else (
    echo Requirements already installed.
)

echo [3/3] Running main.py...
"%VENV_PY%" main.py
exit /b %errorlevel%