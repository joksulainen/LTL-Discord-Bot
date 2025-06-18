import json
from dataclasses import dataclass, field
from typing import Self, Any


@dataclass(kw_only=True, eq=False)
class BaseJSONWrapper:
    """Base class for wrapping a JSON file to a Python object.
    
    `_fp`: File path to the JSON file that this object wraps.
    
    `_data`: Additional data that should be in the JSON but aren't or shouldn't be in the dataclass."""
    _fp: str = field(hash=False, compare=False)
    _data: dict[str, Any] = field(default_factory=dict, hash=False, compare=False)
    
    
    def update(self: Self, *, cls: type[json.JSONEncoder] | None = None, **kwargs) -> None:
        """Updates the fields using the given kwargs. Keys that don't match a field are ignored.
        
        `cls`: A JSONEncoder class that will be used to encode the class to JSON with."""
        for k, v in kwargs.items():
            if k not in self.__annotations__: continue
            setattr(self, k, v)
        data: dict[str, Any] = {k:v for k,v in self.__dict__.items() if not (k=="_fp" or k=="_data")}
        data.update(self._data.items())
        with open(self._fp, "w") as file:
            json.dump(data, file, indent=4, cls=cls)
    
    @classmethod
    def create_from_json(_cls: type[Self], fp: str, *, cls: type[json.JSONDecoder] | None = None, **kwargs) -> Self | None:
        """Creates an object using the given file path. Returns `None` if file path doesn't exist or isn't JSON.
        
        `cls`: A JSONDecoder class that will be used to decode the JSON to Python objects with."""
        try:
            with open(fp, "r") as file:
                data: dict[str, Any] = json.load(file, cls=cls, **kwargs)
        except FileNotFoundError:
            return None
        _data = {k:v for k,v in data.items() if k not in _cls.__annotations__}
        return _cls(_fp=fp, _data=_data, **{k:v for k,v in data.items() if k in _cls.__annotations__})
