
from pydantic import BaseModel
from typing import Optional


#  Address Schema
class ClassRoomRequest(BaseModel):
    name: str