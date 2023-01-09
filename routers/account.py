from fastapi import FastAPI, Depends, APIRouter, status
from models.pydantic_models.request.account import (
    StudentRequest,
    StaffRequest,
    Token,
)
from models.pydantic_models.response.account import (
    ListStudentResponse,
    ListStaffResponse,
    AccountQueryParameters,
    FinalStaffResponse,
)
from config.database import get_db
from sqlmodel import Session
from operations import account as functions
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import exc
import exception


router = APIRouter(tags=["Account"], prefix="/account")


# @router.post("/register-student", response_model=FinalStudentResponse)
@router.post(
    "/register-student",
    response_model=ListStudentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_student(student_data: StudentRequest, db: Session = Depends(get_db)):
    """To register the student"""
    try:
        response = functions.register_student(db, student_data)
    except exc.IntegrityError as e:
        exception.IntegrityError(detail=str(e.orig))
    return response


@router.post(
    "/register-staff",
    response_model=ListStaffResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_staff(staff_data: StaffRequest, db: Session = Depends(get_db)):
    """To register the student"""
    try:
        response = functions.register_staff(db, staff_data)
    except exc.IntegrityError as e:
        exception.IntegrityError(detail=str(e.orig))
    return response


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    To login into the school
        * username = Can give the email as username
    """
    response = functions.login_school(db, form_data)
    return response


@router.get("/accounts")
async def get_account(
    query_parameters: AccountQueryParameters = Depends(AccountQueryParameters),
    db: Session = Depends(get_db),
    current_user: FinalStaffResponse = Depends(functions.get_current_active_staff_user),
    # skip: int = 0,
    # limit: int = 100,
):
    """You can give what ever you want"""
    query_parameters = query_parameters.__dict__
    response = functions.get_account(db=db, params=query_parameters)
    return response


# @router.get("/get-student", response_model=StudentResponse)
# async def get_student(
#     student_id: int,
#     db: Session = Depends(get_db)
# ):
#     """To get one class room by the id given"""
#     response = functions.get_student(db=db,student_id=student_id)
#     return response


# @router.get("/get-class-student", response_model=list[ListStudentResponse])
# async def get_student(
#     class_room_id: int,
#     db: Session = Depends(get_db)
# ):
#     """To get all students in one class room"""
#     response = functions.get_student(db=db,class_room_id=class_room_id)
#     return response


# @router.get("/get-student/roll-number", response_model=StudentResponse)
# async def get_student_roll_number(
#     student_roll_number: int,
#     db: Session = Depends(get_db)
# ):
#     """To get one student by the roll number given"""
#     response = functions.get_student(db=db,student_roll_number=student_roll_number)
#     return response
