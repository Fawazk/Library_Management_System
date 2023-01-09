from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime


class Library(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student: Optional[int] = Field(foreign_key="account.id")
    book: Optional[int] = Field(foreign_key="book.id")
    is_reserved: bool = Field(default=False)
    is_return: bool = Field(default=False)
    date_of_borrow: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    return_date: datetime = Field(nullable=True)
