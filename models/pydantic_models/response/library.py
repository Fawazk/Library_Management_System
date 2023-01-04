from models.pydantic_models.request.library import FinalLibraryRequest
from datetime import datetime, timezone
from pydantic import BaseModel, validator,EmailStr
from typing import List





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


