from typing import Any, Callable, Dict, Type, Union

from pydantic import BaseModel
from pydantic.fields import ModelField

Params = Dict[str, Any]
FieldGenerator = Callable[[ModelField], Any]
FactoryField = Union[FieldGenerator, Any]


def params(model: Type[BaseModel], overrides: Params) -> Params:
    # def key_fn(field: ModelField) -> str:
    #     return field.alias if by_alias else field.name

    return {
        key: param(key, field, overrides)
        for (key, field) in model.__fields__.items()
    }


def param(key: str, field: ModelField, overrides: Params) -> Any:
    if field.name in overrides:
        return eval_param(overrides[field.name], field)

    if field.default:
        return field.default

    if not field.required:
        return None

    # if can_gen_default(field):
    #     return gen_default(field)

    # if factory:
    #     raise PydactoryError(
    #         f"{factory.__name__} does not define required field {field.name} and no default can be generated for type {field.type_.__class__}"
    #     )
    # else:
    #     raise PydactoryError(
    #         f"No default can be generated for field {field.name} of type {field.type_}"
    #     )


def eval_param(v: FactoryField, field: ModelField):
    return v(field) if callable(v) else v
