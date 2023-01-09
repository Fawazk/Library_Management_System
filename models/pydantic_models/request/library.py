from pydantic import BaseModel
from typing import Optional
from fastapi_mail import ConnectionConfig
from models.pydantic_models.settings import email_settings

#  Address Schema
class LibraryRequest(BaseModel):
    book: int


class FinalLibraryRequest(LibraryRequest):
    student: int


email_config = email_settings()

conf = ConnectionConfig(
    MAIL_USERNAME=email_config.MAIL_USERNAME,
    MAIL_PASSWORD=email_config.MAIL_PASSWORD,
    MAIL_FROM=email_config.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)
