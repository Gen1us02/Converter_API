from pydantic_settings import BaseSettings
from .api_config import APIConfig
from pydantic import Field


class Config(BaseSettings):
    api_config: APIConfig = Field(default_factory=APIConfig)

    @classmethod
    def load(cls) -> "Config":
        return cls()


config = Config.load()
