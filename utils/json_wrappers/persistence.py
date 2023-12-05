import json
import sys
import time
from dataclasses import dataclass, field
from typing import Self


DEFAULT_PERSISTENCE = {
    "participants": list(),
    "event_channel": 0,
    "starting_time": 0.0,
    "ending_time": 0.0
}

@dataclass(kw_only=True)
class Persistence:
    _fp: str
    participants: list[int] = field(default_factory=list)
    event_channel: int
    starting_time: float
    ending_time: float
    
    
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
