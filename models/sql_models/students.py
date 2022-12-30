

from sqlmodel import Field, SQLModel
from typing import Optional


class Students(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    roll_number : int
    name: str
    class_room : Optional[int] = Field(foreign_key="classroom.id")