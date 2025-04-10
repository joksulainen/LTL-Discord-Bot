@echo off

where /Q uv.exe
if ERRORLEVEL 0 (
    echo Running bot using uv
    uv run ./src/main.py
) else if exist "./.venv/Scripts/python.exe" (
    echo Running bot using .venv
    "./.venv/Scripts/python.exe" ./src/main.py
) else (
    echo Running bot using py
    py ./src/main.py
)
