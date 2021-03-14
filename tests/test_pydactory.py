import pytest

from pydantic import BaseModel, Field
from pydactory import PydactoryError, Factory
from hamcrest import assert_that, has_properties  # type:ignore


def test_build_simple_factory():
    class Rect(BaseModel):
        height: int
        width: int

    class RectFactory(Factory[Rect]):
        height = 3
        width = 4

    rect = RectFactory.build()
    assert_that(rect, has_properties(height=3, width=4))


def test_build_overrides():
    class Rect(BaseModel):
        height: int
        width: int

    class RectFactory(Factory[Rect]):
        height = 3
        width = 4

    rect = RectFactory.build(height=2)
    assert_that(rect, has_properties(height=2, width=4))


def test_build_model_with_aliases():
    class Rect(BaseModel):
        height: int = Field(alias="Height")
        width: int = Field(alias="Width")


    class RectFactory(Factory[Rect]):
        height = 3
        width = 4


    rect = RectFactory.build()
    assert_that(rect, has_properties(height=3, width=4))


def test_build_model_with_aliases_and_override():
    class Rect(BaseModel):
        height: int = Field(alias="Height")
        width: int = Field(alias="Width")


    class RectFactory(Factory[Rect]):
        height = 3
        width = 4


    rect = RectFactory.build(height=2)
    assert_that(rect, has_properties(height=2, width=4))


def test_factory_mixins():
    class Order(BaseModel):
        id: int
        amount: int


    class Identifiable:
        id = 1


    class OrderFactory(Factory[Order], Identifiable):
        amount = 2


    order = OrderFactory.build()
    assert_that(order, has_properties(id=1, amount=2))


def test_params():
    class Rect(BaseModel):
        height: int
        width: int


    class RectFactory(Factory[Rect]):
        height = 3
        width = 4


    params = RectFactory.params(alias=False)
    assert params["height"] == 3
    assert params["width"] == 4


def test_params_alias():
    class Rect(BaseModel):
        height: int = Field(alias="Height")
        width: int = Field(alias="Width")


    class RectFactory(Factory[Rect]):
        height = 3
        width = 4


    params = RectFactory.params(alias=True)
    assert params["Height"] == 3
    assert params["Width"] == 4
