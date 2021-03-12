from pydactory import build_default
from tests.support import BookFactory, Language, AuthorFactory, Review, Address
from decimal import Decimal
from hamcrest import assert_that, has_properties  # type:ignore


def test_defaults():
    book = BookFactory.build()
    assert_that(book, has_properties(title="War and Peace", language=Language.RUSSIAN))


def test_casted_attr():
    book = BookFactory.build()
    assert book.dimensions == (Decimal("1.0"), Decimal("2.0"), Decimal("3.0"))


def test_overrides():
    book = BookFactory.build(title="Warren Peas")
    assert book.title == "Warren Peas"


def test_factories():
    author = AuthorFactory.build()
    assert isinstance(author.name, str)
    assert author.likes_cake
    assert author.likes_chocolate_cake is None
    assert isinstance(author.address, Address)
    assert author.preferred_language == Language.ENGLISH
    assert author.dob


def test_build_default():
    rating = build_default(Review, comment="really liked it")

    assert rating.comment == "really liked it"
