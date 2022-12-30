
from pydantic import BaseModel
from typing import Optional


#  Address Schema
class StudentRequest(BaseModel):
    name: str
    class_room : int
