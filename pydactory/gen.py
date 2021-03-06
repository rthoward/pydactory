from typing import Any, Callable, Dict, Optional, Type, Union
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
    bool: lambda _f: False
}

def can_gen_default(field: ModelField) -> bool:
    return field.type_ in GENS


def gen_default(field: ModelField) -> Any:
    return GENS[field.type_](field)


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

    raise PydactoryError(
        f"{factory.__name__} does not define required field {field.name}."
    )

@classmethod
def search_override(cls, key: str) -> Optional[FieldGenerator]:
    return getattr(cls, key, None)

def evaluate_field(v: FactoryField, field: ModelField):
    return v(field) if callable(v) else v
