from fastapi import FastAPI, Depends, APIRouter, status
from models.pydantic_models.request.class_room import ClassRoomRequest
from models.pydantic_models.response.class_room import (
    ClassRoomResponse,
    ClassRoomPathParameters,
)
from models.pydantic_models.response.account import ListStudentResponse
from config.database import get_db
from sqlmodel import Session
from operations import class_room as functions
from operations import account as studentfunctions
from models.pydantic_models.response.account import FinalStaffResponse
from sqlalchemy import exc
import exception


router = APIRouter(tags=["class Room"], prefix="/class-room",dependencies=[Depends(
        studentfunctions.get_current_active_staff_user
    )])


@router.post(
    "/register", response_model=ClassRoomResponse, status_code=status.HTTP_201_CREATED
)
async def register_class_room(
    class_room_data: ClassRoomRequest,
    db: Session = Depends(get_db)
):
    """To add the class room"""
    try:
        response = functions.register_class_room(db, class_room_data)
    except exc.IntegrityError as e:
        exception.IntegrityError(detail=str(e.orig))
    return response


@router.get(
    "/students/{ClassRoomId}",
    response_model=list[ListStudentResponse],
    status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
)
async def get_student(
    path_parameters: ClassRoomPathParameters = Depends(ClassRoomPathParameters),
    db: Session = Depends(get_db)
):
    """To get all students in one class room"""
    path_parameters = path_parameters.__dict__
    response = studentfunctions.get_account(db=db, params=path_parameters)
    return response


# @router.get("/list-class-rooms", response_model=list[ClassRoomResponse])
# async def get_class_room(
#     skip:int = 0,
#     limit:int = 100,
#     db: Session = Depends(get_db),
# ):
#     """To get one class room by the id given"""
#     response = functions.get_class_room(db=db,skip=skip,limit=limit)
#     return response


# @router.get("/get-class-room", response_model=list[ClassRoomResponse])
# async def get_class_rooms(
#     class_room_id: int,
#     db: Session = Depends(get_db),
# ):
#     """To get one class room by the id given"""
#     response = functions.get_class_room(db=db,class_room_id=class_room_id)
#     return response
