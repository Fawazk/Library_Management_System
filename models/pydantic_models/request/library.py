
from pydantic import BaseModel
from typing import Optional


#  Address Schema
class LibraryRequest(BaseModel):
    student : int
    book : int
