from fastapi import Depends, APIRouter, BackgroundTasks,Path
from models.pydantic_models.request.book import BookRequest
from models.pydantic_models.response.book import BookResponse
from config.database import get_db
from sqlmodel import Session
from operations import book as functions
from sqlalchemy import exc
import exception


router = APIRouter(tags=["book"], prefix="/book")


@router.post("/register", response_model=BookResponse)
async def register_book(book_data: BookRequest, db: Session = Depends(get_db)):
    """To register the book"""
    try:
        response = functions.register_book(db, book_data)
    except exc.IntegrityError as e:
        exception.IntegrityError(status_code=409, detail=str(e.orig))
    return response


# @router.get("/list-books", response_model=list[BookResponse])
# async def get_book(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db),
# ):
#     """To get one book by the id given"""
#     response = functions.get_book(db=db, skip=skip, limit=limit)
#     return response


# @router.get("/get-book", response_model=BookResponse)
# async def get_books(
#     book_id: int,
#     db: Session = Depends(get_db),
# ):
#     """To get one book by the id given"""
#     response = functions.get_book(db=db,book_id=book_id)
#     return response


@router.patch("/edit/{book_id}", response_model=BookResponse)
async def edit_book(
    book_data: BookRequest,
    backgroud_task: BackgroundTasks,
    book_id: int = Path(title="The ID of the book to get",ge=1),
    db: Session = Depends(get_db),
):
    """To edit the book data book which filtered by given id"""
    response = functions.edit_book(db, book_data, book_id,backgroud_task)
    return response


@router.delete("/delete/{book_id}")
async def delete_book(
    db: Session = Depends(get_db),
    book_id:int = Path(title="The ID of the book to get",ge=1),
    ):
    response = functions.delete_book(db, book_id)
    return response
