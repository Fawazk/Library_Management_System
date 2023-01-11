from fastapi import FastAPI, Depends, APIRouter, Path, BackgroundTasks, status
from operations import library as functions
from models.pydantic_models.request.library import LibraryRequest
from models.pydantic_models.response.library import (
    LibraryResponse,
    EmailSchema,
    LibraryPathParameters,
)
from config.database import get_db
from sqlmodel import Session
from models.pydantic_models.response.account import (
    FinalStudentResponse,
    FinalStaffResponse,
)
from operations import account as studentfunctions


router = APIRouter(tags=["library"], prefix="/library")


@router.post(
    "/borrow", response_model=LibraryResponse, status_code=status.HTTP_201_CREATED
)

async def borrow_book(
    borrow_book_data: LibraryRequest,
    backgroud_task: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: FinalStudentResponse = Depends(
        studentfunctions.get_current_active_user
    ),
):
    """To borrow book from library"""
    response = functions.borrow_book(db, current_user, borrow_book_data, backgroud_task)
    return response


@router.patch("/return-borrow/{BorrowId}", status_code=status.HTTP_202_ACCEPTED)
async def return_borrow_book(
    backgroud_task: BackgroundTasks,
    path_parameters: LibraryPathParameters = Depends(LibraryPathParameters),
    db: Session = Depends(get_db),
    current_user: FinalStudentResponse = Depends(
        studentfunctions.get_current_active_user
    ),
):
    """Return borrowed book to library"""
    response = functions.return_borrow_book(
        db, current_user, path_parameters.borrow_id, backgroud_task
    )
    return response


@router.patch(
    "/borrow-reserved/{ReservedId}",
    response_model=LibraryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def borrow_reserved_book(
    backgroud_task: BackgroundTasks,
    reserved_id: int = Path(
        title="The ID of the reserved book to get",
        description="The ID of the reserved book to get",
        ge=1,
    ),
    db: Session = Depends(get_db),
    current_user: FinalStudentResponse = Depends(
        studentfunctions.get_current_active_user
    ),
):
    """Borrow reserved book from library"""
    response = functions.borrow_reserved_book(
        db, current_user, reserved_id, backgroud_task
    )
    return response


@router.get(
    "/all-data",
    response_model=list[LibraryResponse],
    status_code=status.HTTP_202_ACCEPTED,
)
async def get_library_data(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: FinalStaffResponse = Depends(
        studentfunctions.get_current_active_staff_user
    ),
):
    """To get all the datas inside library"""
    response = functions.get_library_data(db=db, skip=skip, limit=limit)
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


# @router.post('/send-email/backgroundtasks')
# def send_email(email:EmailSchema,background_tasks: BackgroundTasks):
#     functions.send_email(email,background_tasks)
#     return 'Success'
