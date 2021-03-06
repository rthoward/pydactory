from typing import Any, Callable, Dict, Generic, Optional, Type, TypeVar, Union, get_args

from pydantic import BaseModel
from pydantic.fields import ModelField

from pydactory.errors import PydactoryError
from pydactory.fake import FakeGen, Faker

FieldGenerator = Callable[[ModelField], Any]
FactoryField = Union[FieldGenerator, Any]

T = TypeVar("T", bound=BaseModel)

GENS: Dict[Type, Callable[[ModelField], Any]] = {
    str: lambda _f: "fake",
    int: lambda _f: 1,
    list: lambda _f: [],
    bool: lambda _f: False
}

def can_gen(field: ModelField) -> bool:
    return field.type_ in GENS


def gen(field: ModelField) -> Any:
    return GENS[field.type_](field)


class Factory(Generic[T]):
    Fake = FakeGen()

    @classmethod
    def build(cls, **overrides) -> T:
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
    def _model(cls) -> Type[T]:
        model_cls: Type[T] = get_args(cls.__orig_bases__[0])[0]  # type: ignore

        try:
            assert isinstance(model_cls, type(BaseModel))
            return model_cls
        except AssertionError:
            raise PydactoryError(f"Type argument required for {cls.__name__}. Must be subclass of pydantic.BaseModel.")

    @classmethod
    def _generate_field(cls, key: str, field: ModelField, overrides: dict) -> Any:
        if field.name in overrides:
            return cls._evaluate_field(overrides[field.name], field)

        if hasattr(cls, key):
            return cls._evaluate_field(getattr(cls, key), field)

        if field.default:
            return field.default

        if not field.required:
            return None

        if can_gen(field):
            return gen(field)

        raise PydactoryError(
            f"{cls.__name__} does not define required field {field.name}."
        )

    @classmethod
    def _search_override(cls, key: str) -> Optional[FieldGenerator]:
        return getattr(cls, key, None)

    @classmethod
    def _evaluate_field(cls, v: FactoryField, field: ModelField):
        return v(field) if callable(v) else v
