from .base_config import BaseConfig, SettingsConfigDict


class APIConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="api_")

    key: str
    base_url: str
