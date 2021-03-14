import pytest

from pydantic.main import BaseModel
from pydactory import PydactoryError, Factory
from hamcrest import assert_that, has_properties  # type:ignore


def test_build_simple_factory():
    class Square(BaseModel):
        height: int
        width: int

    class SquareFactory(Factory[Square]):
        height = 3
        width = 4

    square = SquareFactory.build()
    assert_that(square, has_properties(height=3, width=4))


def test_build_overrides():
    class Square(BaseModel):
        height: int
        width: int

    class SquareFactory(Factory[Square]):
        height = 3
        width = 4

    square = SquareFactory.build(height=2)
    assert_that(square, has_properties(height=2, width=4))
