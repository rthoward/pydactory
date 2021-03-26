from typing import Any, Callable, Dict, TypeVar, Union

from pydantic import BaseModel

Params = Dict[str, Any]
FieldGenerator = Callable[[], Any]
FactoryField = Union[FieldGenerator, Any]

Model = TypeVar("Model", bound=BaseModel)
