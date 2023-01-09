from pydantic import BaseSettings
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


class EmailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str

    class Config:
        env_file = ".env"


@lru_cache
def email_settings():
    email_settings = EmailSettings()
    return email_settings


@lru_cache
def settings():
    settings = Settings()
    return settings


# def email_settings():
#     email_settings=EmailSettings()
#     return email_settings
# def settings():
#     settings = Settings()
#     return settings
