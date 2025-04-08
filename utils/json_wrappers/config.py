import json
import sys
from dataclasses import dataclass, field
from typing import Self

from .base import BaseJSONWrapper


DEFAULT_CONFIG = {
    "$schema": "./ltl-bot-config.schema.json",
    "token": "",
    "guild_id": 0,
    "afk_interval_min_mins": 15.0,
    "afk_interval_max_mins": 30.0,
    "admin_ids": list(),
}

@dataclass(kw_only=True)
class Config(BaseJSONWrapper):
    token: str
    guild_id: int
    afk_interval_min_mins: float = 15.0
    afk_interval_max_mins: float = 30.0
    admin_ids: list[int] = field(default_factory=list)
    
    
    def __post_init__(self):
        self._data["$schema"] = DEFAULT_CONFIG["$schema"]


# Helper functions
def create_config(fp: str, *, handle_write: bool = False) -> Config | None:
    """Creates a `Config` object using the given file path and returns it. Returns `None` if file path doesn't exist.
    
    Optional `handle_write` kwarg makes function do file writing and program exiting."""
    config = Config.create_from_json(fp)
    if not handle_write: return config
    if config is None:
        with open(fp, "w") as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
        print(f"Created new config at '{fp}'. Fill out the 'token' and 'guild_id' fields before starting the script again.\n" \
                "Not doing so will cause the script to run into an error.")
        sys.exit()
    return config

def update_config(config: Config, **kwargs) -> None:
    """Updates provided `Config` object using provided kwargs and writes it to file."""
    config.update(**kwargs)
