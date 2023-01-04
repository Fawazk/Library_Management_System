from sqlmodel import Field, SQLModel
from typing import Optional


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject: str = Field(default=None, unique=True)
    name: str
    quantity: Optional[int]
