from tests.support import BookFactory


def test_defaults():
    book = BookFactory.build()
    assert book.title == "War and Peace"
    assert len(book.reviews) == 1


def test_overrides():
    book = BookFactory.build(title="Warren Peas")
    assert book.title == "Warren Peas"
