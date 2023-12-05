import json
import sys
import os
from dataclasses import dataclass, field
from typing import Self


DEFAULT_CONFIG = {
    "token": "",
    "guild_id": 0,
    "admin_ids": list(),
    "moderator_ids": list(),
    "afk_interval_min_mins": 10.0,
    "afk_interval_max_mins": 20.0
}

@dataclass(kw_only=True)
class Config:
    _fp: str
    token: str
    guild_id: int
    admin_ids: list[int] = field(default_factory=list)
    moderator_ids: list[int] = field(default_factory=list)
    afk_interval_min_mins: float = field(default=DEFAULT_CONFIG["afk_interval_min_mins"])
    afk_interval_max_mins: float = field(default=DEFAULT_CONFIG["afk_interval_max_mins"])
    
    
    def update(self: Self, **kwargs) -> None:
        """Updates the fields using the given kwargs. Keys that don't match a field are ignored."""
        for k, v in kwargs.items():
            if getattr(self, k, None) is None: continue
            setattr(self, k, v)
        with open(self._fp, "w") as file:
            json.dump({k:v for k,v in self.__dict__.items() if k!="_fp"}, file, indent=4)
    
    @classmethod
    def create_from_json(cls: type[Self], fp: str) -> Self | None:
        """Creates an object using the given file path. Returns `None` if file path doesn't exist or isn't json."""
        try:
            with open(fp, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return None
        return cls(_fp=fp, **data)


# Helper functions
def create_config(fp: str, *, handle_write: bool = False) -> Config | None:
    """Creates a `Config` object using the given file path and returns it. Returns `None` if file path doesn't exist.
    
    Optional `handle_write` kwarg makes function do file writing and program exiting."""
    config = Config.create_from_json(fp)
    if not handle_write: return config
    if config is None:
        with open(fp, "w") as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
        print(f"Created new config at '{fp}'. Fill out the 'token' and 'guild_id' fields before starting the script again.\n"\
                "Not doing so will cause the script to run into an error.")
        os.system("pause")
        sys.exit()

def update_config(config: Config, **kwargs) -> None:
    """Updates provided `Config` object using provided kwargs and writes it to file."""
    config.update(**kwargs)
