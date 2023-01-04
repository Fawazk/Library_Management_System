from sqlmodel import Field, SQLModel
from typing import Optional


class Students(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    roll_number: int
    name: str
    class_room: Optional[int] = Field(foreign_key="classroom.id")
    email: str = Field(default=None, unique=True)
    password: str
    is_active: Optional[bool] = Field(default=True)
    is_super_user: Optional[bool] = Field(default=False)
