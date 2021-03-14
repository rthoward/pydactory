from typing import Any, Dict, Generic, Type, TypeVar, get_args

from pydantic import BaseModel

from pydactory.errors import PydactoryError
from pydactory.fake import FakeGen
from pydactory import gen

T = TypeVar("T", bound=BaseModel)

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
        return gen.build_fields(cls._model(), overrides)

    @classmethod
    def params(cls, **overrides) -> Dict[str, Any]:
        return gen.build_fields(cls._model(), {**cls._field_overrides(), **overrides})

    @classmethod
    def _model(cls) -> Type[T]:
        model_cls: Type[T] = get_args(cls.__orig_bases__[0])[0]  # type: ignore

        try:
            assert isinstance(model_cls, type(BaseModel))
            return model_cls
        except AssertionError:
            raise PydactoryError(f"Type argument required for {cls.__name__}. Must be subclass of pydantic.BaseModel.")

    @classmethod
    def _field_overrides(cls) -> Dict[str, Any]:
        return {key: getattr(cls, key) for key, override in cls._model().__fields__.items() if hasattr(cls, key)}


# def build_default(model: Type[T], **overrides) -> T:
#     return model(**gen.build_fields(model, factory=None, overrides=overrides, by_alias=True))
