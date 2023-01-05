from models.pydantic_models.request.library import FinalLibraryRequest
from datetime import datetime, timezone
from pydantic import BaseModel, validator, EmailStr
from typing import List
from fastapi import Path


#  Address Schema
class LibraryResponse(FinalLibraryRequest):
    id: int
    is_reserved: bool
    is_return: bool
    date_of_borrow: datetime
    return_date: datetime | None = None

    class Config:
        orm_mode = True


class EmailSchema(BaseModel):
    email: List[EmailStr]


class LibraryPathParameters:
    def __init__(
        self,
        borrow_id: int = Path(
            alias="BorrowId",
            title="The ID of the borrow to get",
            description="The ID of the borrow to get",
            ge=1,
        )
    ):
        self.borrow_id = borrow_id
