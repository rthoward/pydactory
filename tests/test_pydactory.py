import pytest
from hamcrest import assert_that, has_properties  # type:ignore
from pydantic import BaseModel, Field
from datetime import datetime

from pydactory import Factory, PydactoryError
from tests.support import Language


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


def test_build_with_callable_param():
    class User(BaseModel):
        id: int

    class UserFactory(Factory[User]):
        id = lambda _: 123

    user = UserFactory.build()
    assert user.id == 123


@pytest.mark.parametrize(
    "type_,expected",
    [
        (int, 1),
        (str, "fake"),
        (bool, False),
        (Language, Language.ENGLISH),
        (datetime, datetime(2000, 1, 1)),
    ],
)
def test_build_default_values(type_, expected):
    class Thing(BaseModel):
        value: type_

    class ThingFactory(Factory[Thing]):
        id = lambda _: 123

    user = ThingFactory.build()
    assert user.value == expected


def test_build_default_values_unknown_throws_exception():
    class Foo:
        pass

    class Bar(BaseModel):
        foo: Foo

        class Config:
            arbitrary_types_allowed = True

    class BarFactory(Factory[Bar]):
        pass

    with pytest.raises(PydactoryError) as e:
        BarFactory.build()

    assert isinstance(e.value, PydactoryError)


def test_build_nested_factory():
    class Foo(BaseModel):
        pass

    class Bar(BaseModel):
        foo: Foo

    class FooFactory(Factory[Foo]):
        pass

    class BarFactory(Factory[Bar]):
        foo = FooFactory

    bar = BarFactory.build()
    assert isinstance(bar.foo, Foo)


def test_build_nested_model():
    class Foo(BaseModel):
        x: int

    class Bar(BaseModel):
        foo: Foo

    class BarFactory(Factory[Bar]):
        foo = Foo

    bar = BarFactory.build()
    assert isinstance(bar.foo, Foo)
    assert bar.foo.x == 1


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
