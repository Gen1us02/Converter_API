from .base_config import BaseConfig, SettingsConfigDict


class AuthConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="auth_")

    secret_key: str
    algorithm: str
    access_token_expire_minutes: str
