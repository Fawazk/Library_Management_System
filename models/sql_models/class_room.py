

from sqlmodel import Field, SQLModel
from typing import Optional


class ClassRoom(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None, unique=True)