from fastapi import Depends, APIRouter, BackgroundTasks, status
from models.pydantic_models.request.book import BookRequest
from models.pydantic_models.response.book import BookResponse, BookPathParameters
from config.database import get_db
from sqlmodel import Session
from operations import book as functions
from sqlalchemy import exc
import exception
from operations import account as studentfunctions
from models.pydantic_models.response.account import FinalStaffResponse


router = APIRouter(tags=["book"], prefix="/book")


@router.post(
    "/register", response_model=BookResponse, status_code=status.HTTP_201_CREATED
)
async def register_book(
    book_data: BookRequest,
    backgroud_task: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: FinalStaffResponse = Depends(
        studentfunctions.get_current_active_staff_user
    ),
):
    """
    ### To register the book
        * Subject must be any one from this ['english', 'maths', 'science', 'social']
    """
    try:
        response = functions.register_book(db, book_data,backgroud_task)
    except exc.IntegrityError as e:
        exception.IntegrityError(detail=str(e.orig))
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


@router.patch(
    "/edit/{BookId}", response_model=BookResponse, status_code=status.HTTP_202_ACCEPTED
)
async def edit_book(
    book_data: BookRequest,
    backgroud_task: BackgroundTasks,
    path_parameters: BookPathParameters = Depends(BookPathParameters),
    db: Session = Depends(get_db),
    current_user: FinalStaffResponse = Depends(
        studentfunctions.get_current_active_staff_user
    ),
):
    """To edit the book"""
    response = functions.edit_book(
        db, book_data, path_parameters.book_id, backgroud_task
    )
    return response


@router.delete("/delete/{BookId}", status_code=status.HTTP_202_ACCEPTED)
async def delete_book(
    db: Session = Depends(get_db),
    path_parameters: BookPathParameters = Depends(BookPathParameters),
    current_user: FinalStaffResponse = Depends(
        studentfunctions.get_current_active_staff_user
    ),
):
    """To delete book"""
    response = functions.delete_book(db, path_parameters.book_id)
    return response
