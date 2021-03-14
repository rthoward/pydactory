from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, Type

from pydantic.fields import ModelField

GENS: Dict[Type, Callable[[ModelField], Any]] = {
    str: lambda _f: "fake",
    int: lambda _f: 1,
    list: lambda _f: [],
    bool: lambda _f: False,
    Enum: lambda f: list(f.type_._member_map_.values())[0],
    datetime: lambda f: datetime(2000, 1, 1),
}


def try_gen_default(type_: Type) -> Any:
    for t, fn in GENS.items():
        if type_ == t:
            return fn(type_)

    for t, fn in GENS.items():
        if isinstance(type_, t):
            return fn(type_)

    for t, fn in GENS.items():
        if issubclass(type_, t):
            return fn(type_)


# def build_model(model: Type[BaseModel], factory: Any, overrides: Params) -> BaseModel:
#     return model(**build_fields(model, factory, overrides))
