from app.core.config.config import config
from typing import Dict, List
import requests


def get_currency_list() -> Dict[str, str]:
    url = config.api_config.base_url + "/list"
    headers = {"apikey": config.api_config.key}
    try:
        response = requests.request("GET", url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get("success"):
            return data["currencies"]
        else:
            raise ValueError("API returned success=False")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request failed: {e}")
    except (KeyError, TypeError) as e:
        raise ValueError(f"Invalid API response: {e}")


def convert(amount: int, from_cur: str, to_cur: str) -> float:
    url = config.api_config.base_url + "/convert"
    headers = {"apikey": config.api_config.key}
    params = {"amount": amount, "from": from_cur, "to": to_cur}
    try:
        response = requests.request("GET", url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("success"):
            return data["result"]
        else:
            raise ValueError("API returned success=False")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request failed: {e}")
    except (KeyError, TypeError) as e:
        raise ValueError(f"Invalid API response: {e}")


def live_currency(curr_list: List[str], from_cur: str) -> Dict[str, float]:
    url = config.api_config.base_url + "/live"
    headers = {"apikey": config.api_config.key}
    params = {"currencies": curr_list, "source": from_cur}
    try:
        response = requests.request("GET", url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("success"):
            return data["quotes"]
        else:
            raise ValueError("API returned success=False")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request failed: {e}")
    except (KeyError, TypeError) as e:
        raise ValueError(f"Invalid API response: {e}")
