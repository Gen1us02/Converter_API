from .base_config import BaseConfig, SettingsConfigDict


class DBConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="db_")

    user: str
    password: str
    name: str
    host: str
    port: int

    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
