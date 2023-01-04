from fastapi import FastAPI
from routers import book, class_room, library, student
from sqlmodel import SQLModel
from config.database import engine


tags_metadata = [
    {"name": "students"},
    {"name": "library"},
    {"name": "book"},
    {"name": "class Room"},
]

description = """
library management system project API helps students do awesome stuff.

## Students

* Student can **Register students**.
* Students must first log into the school if they want to take a book. **Login Students**

## Library

*  By providing the book's ID as params, student can borrow a book, and a text message will be sent to stuent email.
*  when a book is checked out. If a book is unavailable in the library, a reserve has been made for it.
*  Give the borrowed book back. We will send a mailer to all of the reserved students at that time.
*  At that point, reserved students may also borrow the book.
*  We may view all of the library's data. Every aspect of borrowing, reserving, and returning

## Book

* cread operation of book

## Class Room 

* Adding classroom

"""

app = FastAPI(
    openapi_tags=tags_metadata,
    description=description
)


SQLModel.metadata.create_all(engine)

app.include_router(book.router)
app.include_router(class_room.router)
app.include_router(library.router)
app.include_router(student.router)
