from fastapi import APIRouter, HTTPException, status, Query
from typing import Dict, List
from app.utils.external_api import convert, live_currency, get_currency_list

currency_router = APIRouter()


@currency_router.get("/exchange")
async def exchange(
    amount: int = Query(..., description="Amount to convert"),
    from_cur: str = Query(..., description="Source currency code", alias="from"),
    to_cur: str = Query(..., description="Target currency code", alias="to"),
) -> Dict[str, float]:
    try:
        result = await convert(amount=amount, from_cur=from_cur, to_cur=to_cur)
        return {"value": result}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid request: {e}"
        )


@currency_router.get("/live-currency")
async def get_live_currency(
    from_cur: str = Query(..., description="Source currency code"),
    currencies: List[str] = Query(description="List of target currencies", default=[]),
) -> Dict[str, float]:
    try:
        result = await live_currency(curr_list=currencies, from_cur=from_cur)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid request: {e}"
        )


@currency_router.get("/currency-list")
async def currency_list() -> Dict[str, str]:
    try:
        result = await get_currency_list()
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid request: {e}"
        )
