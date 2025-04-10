# Last To Leave Discord Bot

A Discord bot designed around the game of Last to Leave using the py-cord Python library.

This repository is not being actively maintained and is largely a hobby project for whenever I feel like working on it.
I won't be upset if people choose to fork and continue work without me whether it be for themselves or to contribute.

**DISCLAIMER: This project is not production ready and should not be used.**

## How to use

### With uv

1. Install [uv](https://github.com/astral-sh/uv) through your preferred method.
1. Run `Start bot.bat` once.
    - Use the `.sh` script on Linux based systems.
1. Open `config.json` and fill `token` and `guild_id` fields.
1. Run `Start bot.bat` again.

### Without uv

1. Install [Python 3.13](https://www.python.org/downloads/) through your preferred method.
1. Install program dependencies.
    - Run `pip install -r ./requirements.txt` in project root, preferably in a virtual environment to not bloat the system install.
1. Run `Start bot.bat` once.
    - Use the `.sh` script on Linux based systems.
1. Open `config.json` and fill `token` and `guild_id` fields.
1. Run `Start bot.bat` again.

## How to contribute or continue work

1. Install [Python 3.13](https://www.python.org/downloads/) and [uv](https://github.com/astral-sh/uv) through your preferred method. Not much needs to be said here.
1. Install project dependencies by running `uv sync` in project directory.
1. Off you go to contribute or whatever it is that you will do.
