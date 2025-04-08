import json
from dataclasses import dataclass, field, fields
from typing import Self, Any


@dataclass(kw_only=True)
class BaseJSONWrapper:
    """Base class for wrapping a JSON file to a Python object.
    
    `_fp`: File path to the JSON file that this object wraps.
    
    `_data`: Additional data that should be in the JSON but aren't or shouldn't be in the dataclass."""
    _fp: str
    _data: dict[str, Any] = field(default_factory=dict)
    
    
    def __init__(self: Self, **data):
        self._data = dict(data)
        for field in fields(self):
            del self._data[field.name]
            if field.name in data:
                setattr(self, field.name, data[field.name])
    
    def update(self: Self, *, cls: type[json.JSONEncoder] | None = None, **kwargs) -> None:
        """Updates the fields using the given kwargs. Keys that don't match a field are ignored."""
        for k, v in kwargs.items():
            if getattr(self, k, None) is None: continue
            setattr(self, k, v)
        with open(self._fp, "w") as file:
            json.dump({k:v for k,v in (self._data.items() + self.__dict__.items()) if not (k=="_fp" or k=="_data")}, file, indent=4, cls=cls)
    
    @classmethod
    def create_from_json(cls: type[Self], fp: str, **kwargs) -> Self | None:
        """Creates an object using the given file path. Returns `None` if file path doesn't exist or isn't JSON."""
        try:
            with open(fp, "r") as file:
                data = json.load(file, **kwargs)
        except FileNotFoundError:
            return None
        return cls(_fp=fp, **data)
