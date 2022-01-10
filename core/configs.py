import os
from attr.validators import ge
from pydantic import BaseConfig
from dotenv import load_dotenv
from os import getenv


class Settings:
    def __init__(self) -> None:
        load_dotenv()
        self.URL_DB_ASYNC: str = getenv('URL_DB_ASYNC', None)
        self.DB_POOL_SIZE: int = getenv('DB_POOL_SIZE', None)

    def reload(self):
        load_dotenv()
        self.URL_DB_ASYNC: str = getenv('URL_DB_ASYNC', None)
        self.DB_POOL_SIZE: int = int(getenv('DB_POOL_SIZE', None))


settings = Settings()
