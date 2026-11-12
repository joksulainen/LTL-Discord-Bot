import json
from dataclasses import dataclass, field
from json import JSONDecoder, JSONEncoder
from pathlib import Path
from typing import Any

from .. import LeaderboardEntry
from .base import BaseJSONWrapper

DEFAULT_PERSISTENCE: dict[str, Any] = {
    "$schema": "./ltl-bot-persistence.schema.json",
    "participants": [],
    "event_channel_id": 0,
    "starting_time": 0.0,
    "ending_time": 0.0,
    "leaderboard": []
}

@dataclass(kw_only=True)
class Persistence(BaseJSONWrapper):
    participants: list[int] = field(default_factory=list)
    event_channel_id: int = 0
    starting_time: float = 0.0
    ending_time: float = 0.0
    leaderboard: list[LeaderboardEntry] = field(default_factory=list)
    
    
    def __post_init__(self):
        self._data["$schema"] = DEFAULT_PERSISTENCE["$schema"]


# JSON encoder and decoder classes to handle any classes in the Persistence dataclass
class PersistenceJSONEncoder(JSONEncoder):
    def default(self, o: object):
        if isinstance(o, LeaderboardEntry):
            return (o.user_id, o.eliminated_at)
        return super().default(o)

class PersistenceJSONDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, object_hook=self.object_hook, **kwargs)
    
    def object_hook(self, dct: dict[str, Any]) -> dict[str, Any]:
        if "leaderboard" in dct:
            temp = []
            for item in dct["leaderboard"]:
                temp.append(LeaderboardEntry(item[0], item[1]))
            dct["leaderboard"] = temp
        return dct


# Helper functions
def create_persistence(fp: Path) -> tuple[Persistence, bool]:
    """Creates a `Persistence` object and returns it with success for loading from existing file."""
    persistence = Persistence.create_from_json(fp, cls=PersistenceJSONDecoder)
    success = persistence is not None
    if not success:
        with fp.open("w") as file:
            json.dump(DEFAULT_PERSISTENCE, file, indent=4, cls=PersistenceJSONEncoder)
        persistence = Persistence(_fp=fp, **DEFAULT_PERSISTENCE)
    return persistence, success

def update_persistence(persistence: Persistence, **kwargs) -> None:
    """Updates provided `Persistence` object using provided kwargs and writes it to file."""
    persistence.update(cls=PersistenceJSONEncoder, **kwargs)
