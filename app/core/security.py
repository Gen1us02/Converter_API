import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.config.config import config
import datetime
from typing import Dict


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def generate_jwt_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now() + datetime.timedelta(
        minutes=config.auth_config.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        key=config.auth_config.secret_key,
        algorithm=config.auth_config.algorithm,
    )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(
            token,
            key=config.auth_config.secret_key,
            algorithm=config.auth_config.algorithm,
        )
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token (no subject)")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
