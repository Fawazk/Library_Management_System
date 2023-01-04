from fastapi import FastAPI, Depends, APIRouter, HTTPException, BackgroundTasks
from operations import library as functions
from models.pydantic_models.request.library import LibraryRequest, conf
from models.pydantic_models.response.library import LibraryResponse, EmailSchema
from config.database import get_db
from sqlmodel import Session
from models.pydantic_models.response.student import FinalStudentResponse
from operations import student as studentfunctions

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from models.pydantic_models.response.library import EmailSchema
from starlette.requests import Request
from starlette.responses import JSONResponse

router = APIRouter(tags=["library"], prefix="/library")


@router.post("/borrow-book", response_model=LibraryResponse)
async def borrow_book(
    borrow_book_data: LibraryRequest,
    backgroud_task:BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: FinalStudentResponse = Depends(
        studentfunctions.get_current_active_user
    ),
):
    """To borrow book from library"""
    response = functions.borrow_book(db,current_user,borrow_book_data,backgroud_task)
    return response


@router.patch("/return-borrow-book")
async def return_borrow_book(
    borrow_id: int,
    backgroud_task:BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: FinalStudentResponse = Depends(
        studentfunctions.get_current_active_user
    ),
):
    """Return borrowed book in to library"""
    response = functions.return_borrow_book(db, borrow_id,backgroud_task)
    return response


@router.patch("/borrow-reserved-book", response_model=LibraryResponse)
async def borrow_reserved_book(
    reserved_id: int,
    backgroud_task:BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: FinalStudentResponse = Depends(
        studentfunctions.get_current_active_user
    ),
):
    """Borrow reserved book from library"""
    response = functions.borrow_reserved_book(db, reserved_id,backgroud_task)
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


@router.get("/library-datas", response_model=list[LibraryResponse])
async def get_library_data(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """To get one class room by the id given"""
    response = functions.get_library_data(db=db, skip=skip, limit=limit)
    return response

# @router.post('/send-email/backgroundtasks')
# def send_email(email:EmailSchema,background_tasks: BackgroundTasks):
#     functions.send_email(email,background_tasks)
#     return 'Success'
