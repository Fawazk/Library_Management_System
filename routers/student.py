from fastapi import FastAPI, Depends, APIRouter, HTTPException
from models.pydantic_models.request.student import (
    StudentRequest,
    Token,
    StudentLoginDataRequest,
)
from models.pydantic_models.response.student import (
    FinalStudentResponse,
    ListStudentResponse,
)
from config.database import get_db
from sqlmodel import Session
from operations import student as functions
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import exc
import exception


router = APIRouter(tags=["students"], prefix="/student")


# @router.post("/register-student", response_model=FinalStudentResponse)
@router.post("/register", response_model=ListStudentResponse)
async def register_student(student_data: StudentRequest, db: Session = Depends(get_db)):
    """To register the student
    subject must be any of that which shown in example
    """
    try:
        response = functions.register_student(db, student_data)
    except exc.IntegrityError as e:
        exception.IntegrityError(status_code=409, detail=str(e.orig))
    return response


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """To login into the school
    username = Can give the email as username
    """
    response = functions.login_school(db, form_data)
    return response


# @router.get("/list-students", response_model=list[ListStudentResponse])
# async def get_students(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(get_db),
# ):
#     """To get one class room by the id given"""
#     response = functions.get_student(db=db, skip=skip, limit=limit)
#     return response


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
