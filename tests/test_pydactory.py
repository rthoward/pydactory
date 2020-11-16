from tests.support import BookFactory


def test_defaults():
    book = BookFactory.build()
    assert book.title == "War and Peace"
