from pydantic_settings import BaseSettings
from .api_config import APIConfig
from .db_config import DBConfig
from pydantic import Field


class Config(BaseSettings):
    api_config: APIConfig = Field(default_factory=APIConfig)
    db_config: DBConfig = Field(default_factory=DBConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()


config = Config.load()
