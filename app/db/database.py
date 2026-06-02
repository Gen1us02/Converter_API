from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config.config import config


engine = create_async_engine(url=config.db_config.ASYNC_DATABASE_URL)
async_session = async_sessionmaker(engine, class_=AsyncSession)


async def get_session():
    async with async_session() as session:
        yield session
