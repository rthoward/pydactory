from tests.support import BookFactory
from decimal import Decimal
from hamcrest import assert_that, has_properties  # type:ignore


def test_defaults():
    book = BookFactory.build()
    assert_that(book, has_properties(title="War and Peace", author="Leo Tolstoy"))


def test_casted_attr():
    book = BookFactory.build()
    assert book.dimensions == (Decimal("1.0"), Decimal("2.0"), Decimal("3.0"))


def test_overrides():
    book = BookFactory.build(title="Warren Peas")
    assert book.title == "Warren Peas"
