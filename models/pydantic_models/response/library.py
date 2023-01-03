
from models.pydantic_models.request.library import LibraryRequest
from datetime import datetime, timezone



#  Address Schema


class LibraryResponse(LibraryRequest):
    id: int
    is_reserved : bool
    is_return : bool
    date_of_borrow: datetime
    return_date: datetime | None = None

    class Config:
        orm_mode = True