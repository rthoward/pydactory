from inspect import isclass, ismethod
from typing import Dict, Type, Any, Optional

from pydantic import BaseModel
from pydantic.fields import ModelField

from pydactory.gen import try_gen_default
from pydactory import errors
from pydactory.types import Model, Params, FactoryField


def kwargs_to_aliases(model: Type[Model], kwargs: Dict[str, Any]) -> Dict[str, Any]:
    def to_alias(k: str) -> Optional[str]:
        try:
            return model.__fields__[k].alias
        except KeyError:
            return None

    return {alias: v for k, v in kwargs.items() if (alias := to_alias(k)) is not None}


def build_model(model: Type[Model], overrides: Params) -> Model:
    return model(**kwargs_to_aliases(model, params(model, overrides)))


def params(model: Type[BaseModel], overrides: Params) -> Params:
    # def key_fn(field: ModelField) -> str:
    #     return field.alias if by_alias else field.name

    return {
        key: param(key, field, overrides) for (key, field) in model.__fields__.items()
    }


def param(key: str, field: ModelField, overrides: Params) -> Any:
    if field.name in overrides:
        override_val = overrides[field.name]

        if ismethod(getattr(override_val, "build", None)):
            return override_val.build()
        elif isclass(override_val) and issubclass(override_val, BaseModel):
            return build_model(override_val, overrides)  # type: ignore
        return eval_param(override_val, field)

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
