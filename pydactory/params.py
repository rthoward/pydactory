from inspect import isclass, ismethod
from typing import Any, Dict, Optional, Type

from pydantic import BaseModel
from pydantic.fields import ModelField

from pydactory import errors
from pydactory.gen import try_gen_default
from pydactory.types import FactoryField, Model, Params


class Unspecified:
    ...


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
    return {
        key: value
        for (key, field) in model.__fields__.items()
        if (value := param(key, field, overrides)) is not Unspecified
    }


def param(key: str, field: ModelField, overrides: Params) -> Any:
    if field.name in overrides:
        override_val = overrides[field.name]

        if ismethod(getattr(override_val, "build", None)):
            return override_val.build()
        elif isclass(override_val) and issubclass(override_val, BaseModel):
            return build_model(override_val, overrides)
        return eval_param(override_val)

    if not field.required or (field.default is not None):
        return Unspecified

    is_generic = field.outer_type_ != field.type_
    is_model = isclass(field.type_) and issubclass(field.type_, BaseModel)

    if is_model and not is_generic:
        return build_model(field.type_, {})

    try:
        return try_gen_default(field.outer_type_)
    except errors.NoDefaultGeneratorError:
        raise errors.NoDefaultGeneratorError(key=key, type_=field.outer_type_)


def eval_param(v: FactoryField):
    return v() if callable(v) else v
