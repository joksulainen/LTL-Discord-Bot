if [ -x "$(command -v uv)" ] then
    echo Running bot using uv
    uv run ./src/main.py
elif [ -f "./.venv/bin/python" ] then
    echo Running bot using .venv
    ./.venv/bin/python ./src/main.py
else
    echo Running bot using python
    python ./src/main.py
fi
