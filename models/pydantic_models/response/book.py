from models.pydantic_models.request.book import BookRequest
from fastapi import Path

#  Address Schema
class BookResponse(BookRequest):
    id: int

    class Config:
        orm_mode = True


class BookPathParameters:
    def __init__(
        self,
        book_id: int = Path(
            alias="BookId",
            title="The ID of the book to get",
            description="The ID of the book to get",
            ge=1
        )
        # library_id : int = Path()
    ):
        self.book_id = book_id
