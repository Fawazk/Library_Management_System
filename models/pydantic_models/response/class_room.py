
from pydantic import BaseModel
from typing import Optional
from models.pydantic_models.request.class_room import ClassRoomRequest



#  Address Schema
class ClassRoomResponse(ClassRoomRequest):
    id: int

    class Config:
        orm_mode = True