
from pydantic import BaseModel,validator
from typing import Optional


#  Address Schema
class BookRequest(BaseModel):
    name: str
    quantity : int

    @validator('quantity')
    def set_quantity(cls, quantity):
        return quantity or 1
    