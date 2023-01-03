from models.pydantic_models.request.library import LibraryRequest
from models.sql_models.library import Library
from models.sql_models.book import Book
from models.sql_models.students import Students
import exception
from datetime import datetime


def borrow_book(db, borrow_book_data: LibraryRequest):
    """This is the function for borrowing book"""
    student_db = db.get(Students,borrow_book_data.student)
    book_db = db.get(Book,borrow_book_data.book)
    if student_db:
        if book_db:            
            book_quantity = book_db.quantity
            if book_quantity > 0:
                borrow_book_data = Library(**borrow_book_data.dict())
                setattr(book_db,'quantity',book_quantity-1)
                db.add(book_db)
                db.commit()
                db.refresh(book_db)
            else:
                borrow_book_data = Library(**borrow_book_data.dict(),is_reserved=True)
            db.add(borrow_book_data)
            db.commit()
            db.refresh(borrow_book_data)
            return borrow_book_data
        else:
            exception.Exception_id_not_found('book')
    else:
        exception.Exception_id_not_found('student')


def return_borrow_book(db,borrow_id):
    Library_db = db.get(Library,borrow_id)
    if Library_db and Library_db.is_reserved == False and Library_db.is_return == False:
        book_db = db.get(Book,Library_db.book)
        setattr(book_db,'quantity',book_db.quantity+1)
        setattr(Library_db,'is_return',True)
        setattr(Library_db,'return_date',datetime.now())
        db.add(book_db)
        db.add(Library_db)
        reserved_library = get_library_data(db=db,is_reserved=True,book=book_db.id)
        if reserved_library:
            reserved_library_db = db.get(Library,reserved_library[0].id)
            setattr(reserved_library_db,'is_reserved',False)
            db.add(reserved_library_db)
        db.commit()
        return {"message": "Thanks for taking book from library keep it up"}
    else:
        exception.Exception_id_not_found('library')


def borrow_reserved_book(db,reserved_id):
    Library_db = db.get(Library,reserved_id)
    if Library_db and Library_db.is_reserved and Library_db.is_return == False:
        book_db = db.get(Book,Library_db.book)
        book_quantity = book_db.quantity
        if book_db:
            if book_quantity > 0:
                setattr(book_db,'quantity',book_quantity-1)
                setattr(Library_db,'is_reserved',False)
                setattr(Library_db,'date_of_borrow',datetime.now())
                db.add(book_db)
                db.add(Library_db)
                db.commit()
                db.refresh(Library_db)
                return Library_db
            else:
                exception.No_book_availabe_still()
        else:
            exception.Exception_id_not_found('book')
    else:
        exception.Exception_id_not_found('library')


def get_library_data(**kwargs):
    if "db" in kwargs:
        db = kwargs["db"]
        if "is_reserved" in kwargs and "book" in kwargs:
            is_reserved = kwargs['is_reserved']
            book_id = kwargs['book']
            list_of_library = db.query(Library).filter(Library.is_reserved == is_reserved).filter(Library.book == book_id).all()
            if list_of_library == []:
                return None
            list_of_library.sort(key = lambda data: data.date_of_borrow)
            return list_of_library
        
        if "library_data_id" in kwargs:
            library_data_id = kwargs['library_data_id']
            list_of_library = db.query(Library).filter(Library.id == library_data_id).first()
            if list_of_library:
                return list_of_library
            else:
                exception.Exception_id_not_found('library')
            
        if "limit" in kwargs and "skip" in kwargs:
            skip = kwargs["skip"]
            limit = kwargs["limit"]
            list_of_library = db.query(Library).offset(skip).limit(limit).all()
        else:
            list_of_library = db.query(Library).all()
        return list_of_library
    else:
        exception.Exception_database_error()