from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .base import BaseJSONWrapper

DEFAULT_CONFIG: dict[str, Any] = {
    "$schema": "./ltl-bot-config.schema.json",
    "guild_id": 0,
    "afk_interval_min_mins": 30.0,
    "afk_interval_max_mins": 60.0,
    "admin_ids": [],
}

@dataclass(kw_only=True)
class Config(BaseJSONWrapper):
    guild_id: int
    afk_interval_min_mins: float = 30.0
    afk_interval_max_mins: float = 60.0
    admin_ids: list[int] = field(default_factory=list)
    
    
    def __post_init__(self):
        self._data["$schema"] = DEFAULT_CONFIG["$schema"]


# Helper functions
def create_config(fp: Path) -> Config | None:
    """Creates a `Config` object using the given file path and returns it. Returns `None` if file path doesn't exist."""
    config = Config.create_from_json(fp)
    return config

def update_config(config: Config, **kwargs) -> None:
    """Updates provided `Config` object using provided kwargs and writes it to file."""
    config.update(**kwargs)
