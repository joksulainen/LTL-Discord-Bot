import json
from dataclasses import dataclass, field
from json import JSONEncoder, JSONDecoder
from typing import Any

from .base import BaseJSONWrapper
from .. import LeaderboardEntry


DEFAULT_PERSISTENCE = {
    "$schema": "./ltl-bot-persistence.schema.json",
    "participants": list(),
    "event_channel_id": 0,
    "starting_time": 0.0,
    "ending_time": 0.0,
    "leaderboard": list()
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
            temp = list()
            for item in dct["leaderboard"]:
                temp.append(LeaderboardEntry(item[0], item[1]))
            dct["leaderboard"] = temp
        return dct


# Helper functions
def create_persistence(fp: str, *, return_success: bool = False) -> Persistence | tuple[Persistence, bool]:
    """Creates a `Persistence` object and returns it.
    
    Optional `return_success` kwarg makes function return success with loading from existing file as well."""
    persistence = Persistence.create_from_json(fp, cls=PersistenceJSONDecoder)
    success = persistence is not None
    if not success:
        with open(fp, "w") as file:
            json.dump(DEFAULT_PERSISTENCE, file, indent=4, cls=PersistenceJSONEncoder)
        persistence = Persistence(_fp=fp, **DEFAULT_PERSISTENCE)
    if return_success:
        return persistence, success
    return persistence

def update_persistence(persistence: Persistence, **kwargs) -> None:
    """Updates provided `Persistence` object using provided kwargs and writes it to file."""
    persistence.update(cls=PersistenceJSONEncoder, **kwargs)
