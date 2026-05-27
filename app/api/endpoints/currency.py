from fastapi import APIRouter, HTTPException, status
from app.utils.external_api import convert, live_currency, get_currency_list
from app.api.schemas.currency import ConvertRequest, LiveCurrencyRequest
from typing import Dict


currency_router = APIRouter()


@currency_router.get("/exchange")
async def exchange(convert_data: ConvertRequest) -> float:
    try:
        result = await convert(**convert_data)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid requets: {e}"
        )


@currency_router.get("/live-currency")
async def get_live_currency(live_curr: LiveCurrencyRequest) -> Dict[str, float]:
    try:
        result = await live_currency(**live_curr)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid requets: {e}"
        )


@currency_router.get("/currency-list")
async def currency_list() -> Dict[str, str]:
    try:
        result = await get_currency_list()
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid requets: {e}"
        )
