from models.pydantic_models.request.book import BookRequest


#  Address Schema
class BookResponse(BookRequest):
    id: int

    class Config:
        orm_mode = True
