
from pydantic import BaseModel,validator
from typing import Optional


#  Address Schema
class BookRequest(BaseModel):
    name: str
    quantity : int
    