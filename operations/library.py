from fastapi import BackgroundTasks, Depends
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from models.sql_models.library import Library
from models.sql_models.book import Book
from models.sql_models.students import Students
import exception
from datetime import datetime
from models.pydantic_models.request.library import LibraryRequest, conf
from operations import student as studentfunctions
from models.pydantic_models.response.library import EmailSchema
from starlette.requests import Request
from starlette.responses import JSONResponse


def send_email(email: EmailSchema, templateData, background_task: BackgroundTasks):
    template = f"""
        <html>
        <body>
<h3>Hi !!!
        <br>{templateData}</h3>
        </body>
        </html>
        """
    message = MessageSchema(
        subject="Library Data",
        # List of recipients, as many as you can pass
        recipients=email.dict().get("email"),
        body=template,
        subtype="html",
    )
    fm = FastMail(conf)
    background_task.add_task(fm.send_message, message)


def borrow_book(
    db,
    current_student,
    borrow_book_data: LibraryRequest,
    background_task: BackgroundTasks,
):
    """This is the function for borrowing book"""
    student_db = current_student
    book_db = db.get(Book, borrow_book_data.book)
    all_library_data = get_library_data(db=db,students=student_db.id)
    if all_library_data:
        for data in all_library_data:
            if data.return_date:
                pass
            else:
                exception.UserAlreadyInLibrary(student_db.name)
    if book_db:
        book_quantity = book_db.quantity
        if book_quantity > 0:
            borrow_book_data = Library(**borrow_book_data.dict(), student=student_db.id)
            setattr(book_db, "quantity", book_quantity - 1)
            template = f"we appreciate you using our book."
            db.add(book_db)
            db.commit()
            db.refresh(book_db)
        else:
            borrow_book_data = Library(
                **borrow_book_data.dict(), is_reserved=True, student=student_db.id
            )
            template = f"We appreciate your interest in borrowing the book, but unfortunately, it is not currently available. We will let you know when it becomes available."
        db.add(borrow_book_data)
        db.commit()
        db.refresh(borrow_book_data)
        email = EmailSchema(email=[student_db.email])
        send_email(email, template, background_task)
        return borrow_book_data
    else:
        exception.Exception_id_not_found("book")


def return_borrow_book(
    db, current_student, borrow_id, background_task: BackgroundTasks
):
    student_db = current_student
    Library_db = db.get(Library, borrow_id)
    if (
        Library_db
        and Library_db.is_reserved == False
        and Library_db.is_return == False
        and Library_db.student == student_db.id
    ):
        book_db = db.get(Book, Library_db.book)
        setattr(book_db, "quantity", book_db.quantity + 1)
        setattr(Library_db, "is_return", True)
        setattr(Library_db, "return_date", datetime.now())
        db.add(book_db)
        db.add(Library_db)
        db.commit()
        db.refresh(book_db)
        template = f"I appreciate you giving the borrowed book back."
        sendemail = EmailSchema(email=[student_db.email])
        send_email(sendemail, template, background_task)
        reserved_library = get_library_data(db=db, is_reserved=True, book=book_db.id)
        if reserved_library:
            for data in reserved_library:
                reserved_student_db = db.get(Students, data.student)
                template_msg = f"The {book_db.name} book you requested is now available. There are {book_db.quantity} quantities available right now, so hurry up and grab one before they are all gone."
                email = EmailSchema(email=[reserved_student_db.email])
                send_email(email, template_msg, background_task)
            # reserved_library_db = db.get(Library, reserved_library[0].id)
            # setattr(reserved_library_db, "is_reserved", False)
            # db.add(reserved_library_db)
        return {"message": "Thanks for taking book from library keep it up"}
    else:
        exception.Exception_id_not_found("library")


def borrow_reserved_book(
    db, current_student, reserved_id, background_task: BackgroundTasks
):
    Library_db = db.get(Library, reserved_id)
    student_db = current_student
    if (
        Library_db
        and Library_db.is_reserved
        and Library_db.is_return == False
        and student_db
        and Library_db.student == student_db.id
    ):
        book_db = db.get(Book, Library_db.book)
        book_quantity = book_db.quantity
        if book_db:
            if book_quantity > 0:
                setattr(book_db, "quantity", book_quantity - 1)
                setattr(Library_db, "is_reserved", False)
                setattr(Library_db, "date_of_borrow", datetime.now())
                db.add(book_db)
                db.add(Library_db)
                db.commit()
                db.refresh(Library_db)
                template = f"we appreciate you using our book."
                email = EmailSchema(email=[student_db.email])
                send_email(email, template, background_task)
                return Library_db
            else:
                templates = f"We appreciate your interest in borrowing the book, but unfortunately, it is not currently available. We will let you know when it becomes available."
                email = EmailSchema(email=[student_db.email])
                send_email(email, templates, background_task)
                exception.No_book_availabe_still()
        else:
            exception.Exception_id_not_found("book")
    else:
        exception.Exception_id_not_found("library")


def get_library_data(**kwargs):
    if "db" in kwargs:
        db = kwargs["db"]
        if "is_reserved" in kwargs and "book" in kwargs:
            is_reserved = kwargs["is_reserved"]
            book_id = kwargs["book"]
            list_of_library = (
                db.query(Library)
                .filter(Library.is_reserved == is_reserved)
                .filter(Library.book == book_id)
                .all()
            )
            if list_of_library == []:
                return None
            list_of_library.sort(key=lambda data: data.date_of_borrow)
            return list_of_library
        
        if "students" in kwargs:
            student_id  = kwargs["students"]
            list_of_library = (
                db.query(Library)
                .filter(Library.student == student_id)
                .all()
            )
            if list_of_library == []:
                return None
            list_of_library.sort(key=lambda data: data.date_of_borrow)
            return list_of_library

        if "library_data_id" in kwargs:
            library_data_id = kwargs["library_data_id"]
            list_of_library = (
                db.query(Library).filter(Library.id == library_data_id).first()
            )
            if list_of_library:
                return list_of_library
            else:
                exception.Exception_id_not_found("library")

        if "limit" in kwargs and "skip" in kwargs:
            skip = kwargs["skip"]
            limit = kwargs["limit"]
            list_of_library = db.query(Library).offset(skip).limit(limit).all()
        else:
            list_of_library = db.query(Library).all()
        return list_of_library
    else:
        exception.Exception_database_error()
