@echo off

REM Check if .venv directory exists
IF NOT EXIST .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate the virtual environment
CALL .venv\Scripts\activate

REM Check if requirements are installed
python -c "import pkg_resources; pkg_resources.require(open('requirements.txt').readlines())" 2> nul
IF ERRORLEVEL 1 (
    echo Installing requirements...
    pip install -r requirements.txt
)

REM Run the main program
python main.py

REM Deactivate the virtual environment
deactivate

echo Done!
