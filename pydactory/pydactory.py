from typing import Any, Callable, Dict, Optional, Type, Union

from pydantic import BaseModel
from pydantic.fields import ModelField

from .errors import PydactoryError
from .fake import FakeGen

FieldGenerator = Callable[[ModelField], Any]
FactoryField = Union[FieldGenerator, Any]


class Factory:
    class Meta:
        model: Optional[Type[BaseModel]] = None

    Fake = FakeGen()

    @classmethod
    def build(cls, **overrides) -> BaseModel:
        """
        Build a valid model instance.
        """
        return cls._model()(**cls.params(**overrides))

    @classmethod
    def construct_params(cls, **overrides) -> Dict[str, Any]:
        overrides = overrides or {}
        return {
            field.name: cls._generate_field(key, field, overrides)
            for (key, field) in cls._model().__fields__.items()
        }

    @classmethod
    def params(cls, **overrides) -> Dict[str, Any]:
        return {
            field.alias: cls._generate_field(key, field, overrides)
            for (key, field) in cls._model().__fields__.items()
        }

    @classmethod
    def _model(cls) -> Type[BaseModel]:
        maybe_model = getattr(cls.Meta, "model", None)
        if maybe_model is None:
            raise PydactoryError(
                "Subclasses of PydanticFactory must provide an inner Meta "
                "class with an attribute `model`"
            )

        try:
            assert isinstance(maybe_model, type(BaseModel))
            return maybe_model
        except AssertionError:
            raise PydactoryError("Meta.model must be a pydantic.BaseModel subclass")

    @classmethod
    def _generate_field(cls, key: str, field: ModelField, overrides: dict) -> Any:
        if field.name in overrides:
            return cls._evaluate_field(overrides[field.name], field)
        elif hasattr(cls, key):
            return cls._evaluate_field(getattr(cls, key), field)
        elif field.required:
            raise PydactoryError(
                f"{cls.__name__} does not define required field {field.name}."
            )
        else:
            return None

    @classmethod
    def _search_override(cls, key: str) -> Optional[FieldGenerator]:
        return getattr(cls, key, None)

    @classmethod
    def _evaluate_field(cls, v: FactoryField, field: ModelField):
        return v(field) if callable(v) else v
