
from models.pydantic_models.request.book import BookRequest
from models.sql_models.book import Book
import exception

def register_book(db, book_data: BookRequest):
    """This is the function for adding the book"""
    book_data_db = Book(**book_data.dict())
    db.add(book_data_db)
    db.commit()
    db.refresh(book_data_db)
    return book_data_db




def get_book(**kwargs):

    if "db" in kwargs:
        db = kwargs["db"]
        if "book_id" in kwargs:
            book_id = kwargs["book_id"]
            list_of_books = db.get(Book, book_id)
            if list_of_books:
                return list_of_books
            else:
                exception.Exception_id_not_found('book')

        if "limit" in kwargs and "skip" in kwargs:
            skip = kwargs["skip"]
            limit = kwargs["limit"]
            list_of_books = db.query(Book).offset(skip).limit(limit).all()
        else:
            list_of_books = db.query(Book).all()
        return list_of_books
    else:
        exception.Exception_database_error()