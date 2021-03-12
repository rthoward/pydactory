from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Tuple, List

from pydantic import BaseModel, Field

from pydactory import Factory


class Language(Enum):
    ENGLISH = "en"
    FRENCH = "fr"
    SPANISH = "es"
    GERMAN = "de"
    RUSSIAN = "ru"


class Review(BaseModel):
    rating: int = Field(alias="Rating")
    comment: Optional[str] = Field(alias="Comment")


class Address(BaseModel):
    street1: str
    street2: str
    city: str
    state: str
    zip: str = Field(max_length=5)


class Author(BaseModel):
    name: str
    address: Address
    likes_cake: bool = Field(default=True)
    likes_chocolate_cake: Optional[bool]
    preferred_language: Language
    dob: datetime


class Book(BaseModel):
    title: str = Field(alias="Title")
    author: Author = Field(alias="Author")
    pages: int = Field(alias="PageCount")
    isbn_10: Optional[str] = Field(alias="ISBN-10")
    isbn_13: str = Field(alias="ISBN-13")
    dimensions: Tuple[Decimal, Decimal, Decimal] = Field(alias="Dimensions")
    publish_date: datetime = Field(alias="PublishDate")
    language: Language = Field(alias="Language")

    reviews: List[Review] = Field(alias="Reviews")

class AuthorFactory(Factory[Author]):
    ...


class BookFactory(Factory[Book]):
    title = "War and Peace"
    author = lambda _: AuthorFactory.build()
    pages = Factory.Fake.pyint(max_value=1000)
    isbn_13 = "978-1400079988"
    dimensions = ["1.0", "2.0", "3.0"]
    language = Language.RUSSIAN
    publish_date = datetime(1869, 1, 1)
    reviews = [Review.construct(rating=1, comment="too long")]

