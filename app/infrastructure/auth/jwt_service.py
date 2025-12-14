from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


class JWTService:
    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + \
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({'exp': expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_access_token(token: str) -> dict:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return None
