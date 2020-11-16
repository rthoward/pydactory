from tests.support import BlankBookFactory, BookFactory


def test_defaults():
    print(BlankBookFactory.build())
