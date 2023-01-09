from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi.param_functions import Form


#  Address Schema
class StudentLoginTokenDataRequest(BaseModel):
    email: EmailStr


class StudentLoginDataRequest(StudentLoginTokenDataRequest):
    password: str


class StaffRequest(StudentLoginDataRequest):
    name: str


class StudentRequest(StaffRequest):
    class_room: int


class Token(BaseModel):
    access_token: str
    token_type: str
