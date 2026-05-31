from pydantic_settings import BaseSettings
from .api_config import APIConfig
from .db_config import DBConfig
from .auth_config import AuthConfig
from pydantic import Field


class Config(BaseSettings):
    api_config: APIConfig = Field(default_factory=APIConfig)
    db_config: DBConfig = Field(default_factory=DBConfig)
    auth_config: AuthConfig = Field(default_factory=AuthConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()


config = Config.load()
