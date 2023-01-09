from sqlmodel import Field, SQLModel
from typing import Optional


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    roll_number: int = Field(nullable=True)
    name: str
    class_room: Optional[int] = Field(foreign_key="classroom.id", nullable=True)
    email: str = Field(default=None, unique=True)
    password: str
    is_active: Optional[bool] = Field(default=True)
    is_staff_user: Optional[bool] = Field(default=False)
