from pydantic import BaseModel, validator
from typing import Optional
import exception

SUBJECT = ["english", "maths", "science", "social"]

#  Address Schema
class BookRequest(BaseModel):
    name: str
    quantity: int
    subject: str

    @validator("subject")
    def subvalidatot(cls, sub):
        if sub not in SUBJECT:
            exception.Subject_Exception_error(SUBJECT)
        else:
            return sub

    class Config:
        schema_extra = {
            "example": {
                "name": "example name",
                "quantity": 0,
                "subject": f"It must be any one from {SUBJECT} this list",
            }
        }
