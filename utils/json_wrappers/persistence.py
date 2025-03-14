import json
import sys
import time
from dataclasses import dataclass, field

from .base import BaseJSONWrapper


DEFAULT_PERSISTENCE = {
    "participants": list(),
    "event_channel": 0,
    "starting_time": 0.0,
    "ending_time": 0.0
}

@dataclass(kw_only=True)
class Persistence(BaseJSONWrapper):
    participants: list[int] = field(default_factory=list)
    event_channel: int = 0
    starting_time: float = 0.0
    ending_time: float = 0.0


# Helper functions
def create_persistence(fp: str, *, return_success: bool = False) -> Persistence | tuple[Persistence, bool]:
    """Creates a `Persistence` object and returns it.
    
    Optional `return_success` kwarg makes function return success with loading from existing file as well."""
    persistence = Persistence.create_from_json(fp)
    success = persistence is not None
    if not success:
        with open(fp, "w") as file:
            json.dump(DEFAULT_PERSISTENCE, file, indent=4)
        persistence = Persistence(_fp=fp, **DEFAULT_PERSISTENCE)
    if return_success:
        return persistence, success
    return persistence

def update_persistence(persistence: Persistence, **kwargs) -> None:
    """Updates provided `Persistence` object using provided kwargs and writes it to file."""
    persistence.update(**kwargs)
