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


class Review(BaseModel):
    rating: int = Field(alias="Rating")
    comment: Optional[str] = Field(alias="Comment")


class Book(BaseModel):
    title: str = Field(alias="Title")
    pages: int = Field(alias="PageCount")
    isbn_10: str = Field(alias="ISBN-10")
    isbn_13: str = Field(alias="ISBN-13")
    dimensions: Tuple[Decimal, Decimal, Decimal] = Field(alias="Dimensions")
    publish_date: datetime = Field(alias="PublishDate")
    language: Language = Field(alias="Language")

    # reviews: List[Review] = Field(alias="Reviews")


class BlankBookFactory(Factory):
    class Meta:
        model = Book


class BookFactory(Factory):
    class Meta:
        model = Book
