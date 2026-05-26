from app.core.config.config import config
from typing import Dict
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
    
if __name__ == "__main__":
    print(get_currency_list())
