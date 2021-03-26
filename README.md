# `pydactory`

`pydactory` is a factory library for [`pydantic`](https://github.com/samuelcolvin/pydantic/) models with an API inspired by [`factory_boy`](https://github.com/FactoryBoy/factory_boy).

## Installation

PyPI: https://pypi.org/project/pydactory/

`pip install pydactory`

## Features

`pydactory` is...

**low boilerplate**: provides default values for many common types. You don't need to tell `pydactory` how to build your `name: str` fields

**familiar**: define your factories like you define your `pydantic` models: in a simple, declarative syntax

## Getting started

### Declare your `pydantic` models

```python
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Address(BaseModel):
    street1: str
    street2: str
    city: str
    state: str
    zip_code: str = Field(max_length=5)


class Author(BaseModel):
    name: str
    address: Address
    date_of_birth: datetime


class Book(BaseModel):
    title: str = Field(alias="Title")
    author: Author = Field(alias="Author")
    pages: int = Field(alias="PageCount")
    publish_date: datetime = Field(alias="PublishDate")
    isbn_13: str = Field(alias="ISBN-13")
    isbn_10: Optional[str] = Field(alias="ISBN-10")
```

### Declare your factories

```python
from pydactory import Factory


class AuthorFactory(Factory[Author]):
    name = "Leo Tolstoy"


class BookFactory(Factory[Book]):
    title = "War and Peace"
    author = AuthorFactory
    publish_date = datetime.today
```

### Use the factories to build your models

```python
def test_book_factory():
    book: Book = BookFactory.build(title="Anna Karenina")
    assert Book(
        title="Anna Karenina",
        author=Author(
            name="Leo Tolstoy",
            address=Address(
                street1="fake", street2="fake", city="fake", state="fake", zip_code="fake"
            ),
            date_of_birth=datetime.datetime(2000, 1, 1, 0, 0),
        ),
        pages=1,
        publish_date=datetime.datetime(2021, 3, 26, 14, 15, 22, 613309),
        isbn_13="fake",
        isbn_10=None,
    ) == book
```

## Roadmap

`pydactory` is still very much in progress.
