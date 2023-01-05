from fastapi import HTTPException, status
from pydantic import ValidationError


def Exception_id_not_found(item_name):
    item_name = item_name
    raise HTTPException(
        status_code=404,
        detail=f"This {item_name} id is not found in our database. pls enter any correct {item_name} id",
    )


def Exception_database_error():
    raise HTTPException(status_code=502, detail="Database error")


def No_book_availabe_still():
    raise HTTPException(
        status_code=404,
        detail="Again your book is not available we will text you when it is available",
    )


def HTTP_401_UNAUTHORIZED(detail):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def IntegrityError(detail):
    raise HTTPException(status_code=409, detail=detail)


def Subject_Exception_error(subjects):
    raise HTTPException(
        status_code=406, detail=f"It must be any of from {subjects} this list"
    )


def Exception_students_null():
    raise HTTPException(
        status_code=200, detail="There are no students in this classroom."
    )


def UserAlreadyInLibrary(student):
    raise HTTPException(
        status_code=409,
        detail=f"{student} You've already borrowed or reserved one book; the rest can be taken after you return that"
    )