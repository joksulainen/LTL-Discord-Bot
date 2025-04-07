import json
from dataclasses import dataclass
from typing import Self


@dataclass(kw_only=True)
class BaseJSONWrapper:
    _fp: str
    
    
    def update(self: Self, **kwargs) -> None:
        """Updates the fields using the given kwargs. Keys that don't match a field are ignored."""
        for k, v in kwargs.items():
            if getattr(self, k, None) is None: continue
            setattr(self, k, v)
        with open(self._fp, "w") as file:
            json.dump({k:v for k,v in self.__dict__.items() if k!="_fp"}, file, indent=4, **kwargs)
    
    @classmethod
    def create_from_json(cls: type[Self], fp: str, **kwargs) -> Self | None:
        """Creates an object using the given file path. Returns `None` if file path doesn't exist or isn't JSON."""
        try:
            with open(fp, "r") as file:
                data = json.load(file, **kwargs)
        except FileNotFoundError:
            return None
        return cls(_fp=fp, **data)
