from pydantic import BaseSettings
from datetime import datetime, timezone
import configaration


class Settings(BaseSettings):
    SECRET_KEY: str = configaration.SECRET_KEY
    ALGORITHM: str = configaration.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES: int = configaration.ACCESS_TOKEN_EXPIRE_MINUTES

    class Config:
        env_file = "configaratin.py"