from app.core.config.config import config
from typing import Dict, List
import httpx


async def get_currency_list() -> Dict[str, str]:
    url = config.api_config.base_url + "/list"
    headers = {"apikey": config.api_config.key}
    with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=url, headers=headers)
            response.raise_for_status()
            data = response.json()
            if data.get("success", False):
                return data["currencies"]

            raise ValueError("API returned success=False")
        except httpx.RequestError as e:
            raise ValueError(f"Request failed: {e}")
        except httpx.HTTPStatusError as e:
            raise ValueError(f"HTTP error: {e}")


async def convert(amount: int, from_cur: str, to_cur: str) -> float:
    url = config.api_config.base_url + "/convert"
    headers = {"apikey": config.api_config.key}
    params = {"amount": amount, "from": from_cur, "to": to_cur}
    with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get("success", False):
                return data["result"]

            raise ValueError("API returned success=False")
        except httpx.RequestError as e:
            raise ValueError(f"Request failed: {e}")
        except httpx.HTTPStatusError as e:
            raise ValueError(f"HTTP error: {e}")


async def live_currency(curr_list: List[str], from_cur: str) -> Dict[str, float]:
    url = config.api_config.base_url + "/live"
    headers = {"apikey": config.api_config.key}
    params = {"currencies": curr_list, "source": from_cur}
    with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if data.get("success", False):
                return data["quotes"]

            raise ValueError("API returned success=False")
        except httpx.RequestError as e:
            raise ValueError(f"Request failed: {e}")
        except httpx.HTTPStatusError as e:
            raise ValueError(f"HTTP error: {e}")
