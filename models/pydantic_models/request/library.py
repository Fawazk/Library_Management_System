from pydantic import BaseModel
from typing import Optional
from fastapi_mail import ConnectionConfig
import configaration

#  Address Schema
class LibraryRequest(BaseModel):
    book: int


class FinalLibraryRequest(LibraryRequest):
    student: int


conf = ConnectionConfig(
    MAIL_USERNAME=configaration.MAIL_USERNAME,
    MAIL_PASSWORD=configaration.MAIL_PASSWORD,
    MAIL_FROM=configaration.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)
