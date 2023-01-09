from fastapi import FastAPI, Form
from routers import account, book, class_room, library
from sqlmodel import SQLModel
from config.database import engine


tags_metadata = [
    {"name": "Account"},
    {"name": "library"},
    {"name": "book"},
    {"name": "class Room"},
]

description = """
## Library Management System project API helps students do awesome stuff.

### Students

* Student can **Register students**.
* Students must first log into the school if they want to take a book. **Login Students**

### Library

*  By providing the book's ID as params, student can borrow a book, and a text message will be sent to stuent email.
*  when a book is checked out. If a book is unavailable in the library, a reserve has been made for it.
*  Give the borrowed book back. We will send a mailer to all of the reserved students at that time.
*  At that point, reserved students may also borrow the book.
*  We may view all of the library's data. Every aspect of borrowing, reserving, and returning

### Book

* cread operation of book

### Class Room 

* Adding classroom

"""
from fastapi import FastAPI, Query



app = FastAPI(openapi_tags=tags_metadata, description=description)



import os



@app.get("/items/")
async def read_items(
    q: str
    | None = Query(
        default=None,
        example="example@gmail.com",
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        deprecated=False,
    )
):

    name = os.environ["MY_NAME"]
    print(f"Hello {name} from Python")
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

SQLModel.metadata.create_all(engine)


app.include_router(book.router)
app.include_router(class_room.router)
app.include_router(library.router)
app.include_router(account.router)
