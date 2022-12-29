

from sqlmodel import Field, SQLModel
from typing import Optional


class Library(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student : Optional[int] = Field(foreign_key="students.id")
    book : Optional[int] = Field(foreign_key="book.id")
    Is_reserved : bool

