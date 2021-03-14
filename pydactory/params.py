from typing import Any, Callable, Dict, Type, Union

from pydantic import BaseModel
from pydantic.fields import ModelField

from pydactory.gen import try_gen_default
from pydactory import errors

Params = Dict[str, Any]
FieldGenerator = Callable[[ModelField], Any]
FactoryField = Union[FieldGenerator, Any]


def params(model: Type[BaseModel], overrides: Params) -> Params:
    # def key_fn(field: ModelField) -> str:
    #     return field.alias if by_alias else field.name

    return {
        key: param(key, field, overrides) for (key, field) in model.__fields__.items()
    }


def param(key: str, field: ModelField, overrides: Params) -> Any:
    if field.name in overrides:
        return eval_param(overrides[field.name], field)

    if field.default:
        return field.default

    if not field.required:
        return None

    try:
        return try_gen_default(field.type_)
    except errors.NoDefaultGeneratorError:
        raise errors.NoDefaultGeneratorError(key=key, type_=field.type_)


def eval_param(v: FactoryField, field: ModelField):
    return v(field) if callable(v) else v
