from pydantic import BaseModel
from typing import Optional
from models.pydantic_models.request.class_room import ClassRoomRequest
from fastapi import Query, Path

#  Address Schema
class ClassRoomResponse(ClassRoomRequest):
    id: int

    class Config:
        orm_mode = True


class ClassRoomPathParameters:
    def __init__(
        self,
        class_room_id: int = Path(
            alias="ClassRoomId",
            title="The ID of the class room to get students",
            description="The ID of the class room to get students",
            ge=1,
        ),
    ):
        self.class_room_id = class_room_id
