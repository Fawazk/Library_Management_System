from fastapi import FastAPI, Depends, APIRouter, HTTPException
from models.pydantic_models.request.student import StudentRequest
from models.pydantic_models.response.student import StudentResponse
from config.database import get_db
from sqlmodel import Session
from operations import student as functions



router = APIRouter(tags=["students"],prefix="/students")



# @router.post("/register-student", response_model=FinalStudentResponse)
@router.post("/register-student")
async def register_student(student_data: StudentRequest, db: Session = Depends(get_db)):
    """To register the student"""
    response = functions.register_student(db, student_data)
    return response


@router.get("/list-student", response_model=list[StudentResponse])
async def get_students(
    skip:int = 0,
    limit:int = 100,
    db: Session = Depends(get_db),
):
    """To get one class room by the id given"""
    response = functions.get_student(db=db,skip=skip,limit=limit)
    return response


@router.get("/get-student", response_model=StudentResponse)
async def get_student(
    class_room_id: int,
    db: Session = Depends(get_db),
):
    """To get one class room by the id given"""
    response = functions.get_student(db=db,class_room_id=class_room_id)
    return response

