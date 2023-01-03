
from fastapi import FastAPI, Depends, APIRouter, HTTPException
from operations import library as functions
from models.pydantic_models.request.library import LibraryRequest
from models.pydantic_models.response.library import LibraryResponse
from config.database import get_db
from sqlmodel import Session
from models.pydantic_models.response.student import FinalStudentResponse
from operations import student as studentfunctions


router = APIRouter(tags=["library"],prefix="/library")


@router.post("/borrow-book",response_model=LibraryResponse)
async def borrow_book(borrow_book_data: LibraryRequest,
        db: Session = Depends(get_db),
        current_user: FinalStudentResponse = Depends(studentfunctions.get_current_active_user),
        ):
    """To borrow book from library"""
    response = functions.borrow_book(db, borrow_book_data)
    return response


@router.patch("/return-borrow-book")
async def return_borrow_book(borrow_id:int,
        db: Session = Depends(get_db),
        current_user: FinalStudentResponse = Depends(studentfunctions.get_current_active_user),
        ):
    """Return borrowed book in to library"""
    response = functions.return_borrow_book(db,borrow_id)
    return response

@router.patch("/borrow-reserved-book",response_model=LibraryResponse)
async def borrow_reserved_book(
    reserved_id:int,
    db:Session = Depends(get_db),
    current_user: FinalStudentResponse = Depends(studentfunctions.get_current_active_user),
    ):
    """Borrow reserved book from library"""
    response = functions.borrow_reserved_book(db,reserved_id)
    return response


# @router.get("/get-library-data", response_model=LibraryResponse)
# async def get_library_data(
#     library_data_id: int,
#     db: Session = Depends(get_db)
# ):
#     """To get one class room by the id given"""
#     response = functions.get_library_data(db=db,library_data_id=library_data_id)
#     # response = functions.get_library_data(db=db,is_reserved=True,book=1)
#     return response


@router.get("/get-list-library-data", response_model=list[LibraryResponse])
async def get_library_data(
    skip:int = 0,
    limit:int = 100,
    db: Session = Depends(get_db)
):
    """To get one class room by the id given"""
    response = functions.get_library_data(db=db,skip=skip,limit=limit)
    return response