from app.api.endpoints.currency import currency_router
from app.api.endpoints.user import auth_router
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.db.database import setup_db, engine
from app.api.exceptions.exception_handlers import (
    http_exception_handler,
    validation_error_handler,
)
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_db()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)

app.include_router(currency_router, prefix="/currency")
app.include_router(auth_router, prefix="/users")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
