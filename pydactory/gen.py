from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, Type, Union
from pydantic import BaseModel
from pydantic.fields import ModelField

from .errors import PydactoryError

FieldGenerator = Callable[[ModelField], Any]
FactoryField = Union[FieldGenerator, Any]
Params = Dict[str, Any]


GENS: Dict[Type, Callable[[ModelField], Any]] = {
    str: lambda _f: "fake",
    int: lambda _f: 1,
    list: lambda _f: [],
    bool: lambda _f: False,
    BaseModel: lambda f: build_model(f.type_, factory=None, overrides={}),
    Enum: lambda f: list(f.type_._member_map_.values())[0],
    datetime: lambda f: datetime(2000, 1, 1)
}

def can_gen_default(field: ModelField) -> bool:
    for type, _ in GENS.items():
        if field.type_ == type or isinstance(field.type_, type) or issubclass(field.type_, type):
            return True

    return False


def gen_default(field: ModelField) -> Any:
    for type, gen_fn in GENS.items():
        if field.type_ == type:
            return gen_fn(field)

    for type, gen_fn in GENS.items():
        if isinstance(field.type_, type):
            return gen_fn(field)

    for type, gen_fn in GENS.items():
        if issubclass(field.type_, type):
            return gen_fn(field)


def build_model(model: Type[BaseModel], factory: Any, overrides: Params) -> BaseModel:
    return model(**build_fields(model, factory, overrides))


def build_fields(model: Type[BaseModel], factory: Any, overrides: Params, by_alias=False) -> Params:
    def key_fn(field: ModelField) -> str:
        return field.alias if by_alias else field.name

    return {
        key_fn(field): build_field(key, field, overrides, factory)
        for (key, field) in model.__fields__.items()
    }


def build_field(key: str, field: ModelField, overrides: Params, factory: Any) -> Any:
    if field.name in overrides:
        return evaluate_field(overrides[field.name], field)

    if factory and hasattr(factory, key):
        return evaluate_field(getattr(factory, key), field)

    if field.default:
        return field.default

    if not field.required:
        return None

    if can_gen_default(field):
        return gen_default(field)

    if factory:
        raise PydactoryError(
            f"{factory.__name__} does not define required field {field.name} and no default can be generated for type {field.type_.__class__}"
        )
    else:
        raise PydactoryError(
            f"No default can be generated for field {field.name} of type {field.type_}"
        )


def evaluate_field(v: FactoryField, field: ModelField):
    return v(field) if callable(v) else v
