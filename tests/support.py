from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Tuple

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


class Book(BaseModel):
    title: str = Field(alias="Title")
    author: str = Field(alias="Author")
    pages: int = Field(alias="PageCount")
    isbn_10: Optional[str] = Field(alias="ISBN-10")
    isbn_13: str = Field(alias="ISBN-13")
    dimensions: Tuple[Decimal, Decimal, Decimal] = Field(alias="Dimensions")
    publish_date: datetime = Field(alias="PublishDate")
    language: Language = Field(alias="Language")

    # reviews: List[Review] = Field(alias="Reviews")


class BookFactory(Factory[Book]):
    title = "War and Peace"
    author = "Leo Tolstoy"
    pages = Factory.Fake.pyint(max_value=1000)
    isbn_13 = "978-1400079988"
    dimensions = ["1.0", "2.0", "3.0"]
    language = Language.RUSSIAN
    publish_date = datetime(1869, 1, 1)
