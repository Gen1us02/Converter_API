from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import Dict, List
from app.utils.external_api import convert, live_currency, get_currency_list
from app.core.security import get_current_user

currency_router = APIRouter()


@currency_router.get("/exchange")
async def exchange(
    amount: int = Query(..., description="Amount to convert"),
    from_cur: str = Query(..., description="Source currency code", alias="from"),
    to_cur: str = Query(..., description="Target currency code", alias="to"),
    user: str = Depends(get_current_user)
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
    user: str = Depends(get_current_user)
) -> Dict[str, float]:
    try:
        result = await live_currency(curr_list=currencies, from_cur=from_cur)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid request: {e}"
        )


@currency_router.get("/currency-list")
async def currency_list(user: str = Depends(get_current_user)) -> Dict[str, str]:
    try:
        result = await get_currency_list()
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid request: {e}"
        )
