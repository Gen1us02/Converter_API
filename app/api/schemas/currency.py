from pydantic import BaseModel
from typing import List


class ConvertRequest(BaseModel):
    amount: int
    from_cur: str
    to_cur: str


class LiveCurrencyRequest(BaseModel):
    curr_list: List[str] = []
    from_cur: str
