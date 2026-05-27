from app.api.endpoints.currency import currency_router
from fastapi import FastAPI
import uvicorn


app = FastAPI()
app.include_router(currency_router, prefix="/currency")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
