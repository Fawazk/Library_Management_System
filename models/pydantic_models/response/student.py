
from pydantic import BaseModel
from typing import Optional
from models.pydantic_models.request.student import StudentRequest



#  Address Schema

class StudentResponse(StudentRequest):
    roll_number:int


class FinalStudentResponse(StudentResponse):
    id: int

    class Config:
        orm_mode = True