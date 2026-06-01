from app.api.endpoints.currency import currency_router
from app.api.endpoints.user import auth_router
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.database import setup_db, engine
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_db()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(currency_router, prefix="/currency")
app.include_router(auth_router, prefix="/users")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
