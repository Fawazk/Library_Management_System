
from models.pydantic_models.request.book import BookRequest
from models.sql_models.book import Book
import exception
from models.sql_models.library import Library
from operations import library as libraryfunctions


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


def edit_book(db,book_data,book_id):
    address = db.get(Book, book_id)
    if address:
        address_data = book_data.dict(exclude_unset=True)
        for key, value in address_data.items():
            setattr(address, key, value)
        db.add(address)
        if address.quantity > 0:
            reserved_library = libraryfunctions.get_library_data(db=db,is_reserved=True,book=book_id)
            if reserved_library:
                for i in range(address.quantity):
                    if len(reserved_library)>i:
                        reserved_library_db = db.get(Library,reserved_library[i].id)
                        setattr(reserved_library_db,'is_reserved',False)
                        db.add(reserved_library_db)
        db.commit()
        db.refresh(address)
        return address
    else:
        exception.Exception_id_not_found('book')