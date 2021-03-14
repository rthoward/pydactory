from typing import Dict, Any, Callable, Union, TypeVar
from pydantic import BaseModel
from pydantic.fields import ModelField


Params = Dict[str, Any]
FieldGenerator = Callable[[ModelField], Any]
FactoryField = Union[FieldGenerator, Any]

Model = TypeVar("Model", bound=BaseModel)
