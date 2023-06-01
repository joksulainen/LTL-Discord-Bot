import json
import sys
import time
from dataclasses import dataclass, field
from typing import Self, Type, Tuple


DEFAULT = {
    "participants": list(),
    "event_channel": 0,
    "starting_time": 0,
    "ending_time": 0
}

@dataclass(kw_only=True)
class Persistence:
    _fp: str
    participants: list[int] = field(default_factory=list)
    event_channel: int
    starting_time: float
    ending_time: float
    
    
    def update(self: Self, **kwargs) -> None:
        for k, v in kwargs.items():
            if getattr(self, k, None) is None: continue
            setattr(self, k, v)
        with open(self._fp, "w") as file:
            file.write(json.dumps({k:v for (k,v) in self.__dict__.items() if k!="_fp"}, indent=4))
    
    @classmethod
    def create_from_json(cls: Type[Self], fp: str) -> Tuple[Self, bool]:
        success = True
        try:
            with open(fp, "r") as file:
                data = json.loads(file.read())
        except FileNotFoundError:
            with open(fp, "w") as file:
                file.write(json.dumps(DEFAULT, indent=4))
            success = False
            data = dict(DEFAULT)
        return cls(_fp=fp, **data), success


# Functions to handle persistent data manipulation
persistence: Persistence = None

def init_persistence(fp: str) -> bool | None:
    """Initialize a Persistence object. Does nothing if a Persistence object is already initialized.
    
    Returns None if nothing happened. Returns True if loaded from existing file."""
    global persistence
    if persistence is not None: return
    persistence, result = Persistence.create_from_json(fp)
    return result

def update_persistence(**kwargs) -> None:
    """Updates persistence using provided kwargs and writes it to file."""
    global persistence
    persistence.update(**kwargs)
