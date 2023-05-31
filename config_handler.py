import json
import sys
from dataclasses import dataclass, field
from typing import Self, Type


DEFAULT = {
    "token": "",
    "guild_id": 0,
    "admin_ids": list(),
    "moderator_ids": list(),
    "afk_interval_min_mins": 15,
    "afk_interval_max_mins": 30
}

@dataclass(kw_only=True)
class Config:
    _fp: str
    token: str
    guild_id: int
    admin_ids: list[int] = field(default_factory=list)
    moderator_ids: list[int] = field(default_factory=list)
    afk_interval_min_mins: int = field(default=DEFAULT["afk_interval_min_mins"])
    afk_interval_max_mins: int = field(default=DEFAULT["afk_interval_max_mins"])
    
    
    def update(self: Self, **kwargs) -> None:
        for k, v in kwargs.items():
            if getattr(self, k, None) is None: continue
            setattr(self, k, v)
        with open(self._fp, "w") as file:
            file.write(json.dumps({k:v for (k,v) in self.__dict__.items() if k!="_fp"}, indent=4))
    
    @classmethod
    def create_from_json(cls: Type[Self], fp: str) -> Self:
        try:
            with open(fp, "r") as file:
                data = json.loads(file.read())
        except FileNotFoundError:
            with open(fp, "w") as file:
                file.write(json.dumps(DEFAULT, indent=4))
            sys.exit(f"Created new config at '{fp}'. Fill out the 'token' and 'guild_id' fields before starting the script again.")
        return cls(_fp=fp, **data)


# Functions to handle config manipulation
config: Config = None

def init_config(fp: str) -> None:
    """Initialize a Config object. Does nothing if a Config object is already initialized."""
    global config
    if config is not None: return
    config = Config.create_from_json(fp)

def reload_config() -> None:
    """Reloads config by loading it from file again."""
    global config
    fp = config._fp
    config = Config.create_from_json(fp)

def update_config(**kwargs) -> None:
    """Updates config using provided kwargs and writes it to file."""
    global config
    config.update(**kwargs)
