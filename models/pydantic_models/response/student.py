
from pydantic import BaseModel,validator
from typing import Optional
from models.pydantic_models.request.student import StudentRequest



#  Address Schema

class StudentResponse(StudentRequest):
    roll_number:int

class FinalStudentResponse(StudentResponse):
    id: int
    is_active: bool = True
    is_super_user: bool = False


    
    class Config:
        orm_mode = True

class ListStudentResponse(StudentResponse):
    pass

    @validator('password')
    def password_validator(cls, v):
        return "********"