from fastapi import FastAPI
from routers import book, class_room, library, student
from sqlmodel import SQLModel
from config.database import engine


tags_metadata = [
    {"name": "students"},
    {"name": "library"},
    {"name": "book"},
    {"name": "class Room"}
]

app = FastAPI(openapi_tags=tags_metadata)

SQLModel.metadata.create_all(engine)

app.include_router(book.router)
app.include_router(class_room.router)
app.include_router(library.router)
app.include_router(student.router)
