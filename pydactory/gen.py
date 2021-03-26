from datetime import datetime
from decimal import Decimal
from enum import Enum
from inspect import isclass
from typing import Any, Callable, Dict, Type

from pydactory import errors

GENS: Dict[Type, Callable[[Type], Any]] = {
    str: lambda _f: "fake",
    int: lambda _f: 1,
    list: lambda _f: [],
    bool: lambda _f: False,
    Enum: lambda f: list(f._member_map_.values())[0],
    datetime: lambda f: datetime(2000, 1, 1),
    Decimal: lambda _: Decimal("1.00"),
}


def try_gen_default(type_: Type) -> Any:
    for t, fn in GENS.items():
        if type_ == t:
            return fn(type_)

    for t, fn in GENS.items():
        if isinstance(type_, t):
            return fn(type_)

    if getattr(type_, "__origin__", None) == tuple:
        return tuple(try_gen_default(t) for t in type_.__args__)

    if getattr(type_, "__origin__", None) == list:
        return []

    if isclass(type_):
        for t, fn in GENS.items():
            if issubclass(type_, t):
                return fn(type_)

    raise errors.NoDefaultGeneratorError()


# def build_model(model: Type[BaseModel], factory: Any, overrides: Params) -> BaseModel:
#     return model(**build_fields(model, factory, overrides))
