from pydantic import BaseModel, validator, EmailStr
from typing import List
from typing import Optional
from models.pydantic_models.request.account import StudentRequest, StaffRequest
from fastapi import Path, Query

#  Address Schema


class StudentResponse(StudentRequest):
    roll_number: int


class FinalStaffResponse(StaffRequest):
    id: int
    is_active: bool = True
    is_staff_user: bool = True


class FinalStudentResponse(StudentResponse):
    id: int
    is_active: bool = True
    is_staff_user: bool = False

    class Config:
        orm_mode = True


class ListStaffResponse(FinalStaffResponse):
    pass

    @validator("password")
    def password_validator(cls, v):
        return "********"


class ListStudentResponse(StudentResponse):
    pass

    @validator("password")
    def password_validator(cls, v):
        return "********"


class AccountQueryParameters:
    def __init__(
        self,
        student_id: int = Query(
            alias="StudentId",
            title="The ID of the student to get",
            description="The ID of the student to get",
            ge=1,
            default=None,
        ),
        staff_id: int = Query(
            alias="StaffId",
            title="The ID of the staff to get",
            description="The ID of the staff to get",
            ge=1,
            default=None,
        ),
        roll_number: int = Query(
            alias="RollNumber",
            title="The roll number of the student to get",
            description="The roll number of the student to get",
            ge=1,
            default=None,
        ),
        list_student: bool = Query(
            alias="ListStuent",
            title="True to show all the students",
            description="True to show all the students",
            default=False,
        ),
        list_staff: bool = Query(
            alias="ListStaff",
            title="True to show all Staffs",
            description="True to show all Staffs",
            default=False,
        ),
    ):
        self.student_id = student_id
        self.staff_id = staff_id
        self.roll_number = roll_number
        self.list_student = list_student
        self.list_staff = list_staff
