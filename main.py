from fastapi import FastAPI
from routers import book, class_room, library, students
from sqlmodel import SQLModel
from config.database import engine


app = FastAPI()
SQLModel.metadata.create_all(engine)

app.include_router(book.router)
app.include_router(class_room.router)
app.include_router(library.router)
app.include_router(students.router)
