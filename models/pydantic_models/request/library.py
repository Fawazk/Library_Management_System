from pydantic import BaseModel
from typing import Optional
from fastapi_mail import ConnectionConfig


#  Address Schema
class LibraryRequest(BaseModel):
    book: int


class FinalLibraryRequest(LibraryRequest):
    student: int


conf = ConnectionConfig(
   MAIL_USERNAME='fawazfkp2@gmail.com',
   MAIL_PASSWORD="cisodcgsesjmfaks",
   MAIL_FROM="fawazfkp2@gmail.com",
   MAIL_PORT=587,
   MAIL_SERVER="smtp.gmail.com",
   MAIL_STARTTLS=True,
   MAIL_SSL_TLS=False
)