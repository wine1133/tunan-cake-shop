import base64
import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, Header

from common.exception_handler import CustomException
from settings import SECRET_KEY, TOKEN_EXPIRE_HOURS

ALGORITHM = "HS256"
PBKDF2_ITERATIONS = 260_000


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return "pbkdf2_sha256${}${}${}".format(
        PBKDF2_ITERATIONS,
        base64.urlsafe_b64encode(salt).decode("ascii"),
        base64.urlsafe_b64encode(digest).decode("ascii"),
    )


def verify_password(password: str, encoded: str | None) -> bool:
    if not encoded:
        return False
    if not encoded.startswith("pbkdf2_sha256$"):
        # Compatibility for the tutorial's plain-text seed accounts.
        return hmac.compare_digest(password, encoded)
    try:
        _, iterations, salt_b64, digest_b64 = encoded.split("$", 3)
        salt = base64.urlsafe_b64decode(salt_b64.encode("ascii"))
        expected = base64.urlsafe_b64decode(digest_b64.encode("ascii"))
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, int(iterations)
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def create_token(account_id: int, role: str, name: str, username: str) -> str:
    payload = {
        "sub": str(account_id),
        "role": role,
        "name": name,
        "username": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError as exc:
        raise CustomException("登录已过期，请重新登录", "401") from exc
    except jwt.InvalidTokenError as exc:
        raise CustomException("登录状态无效，请重新登录", "401") from exc


async def get_optional_account(authorization: str | None = Header(default=None)) -> dict | None:
    if not authorization or not authorization.lower().startswith("bearer "):
        return None
    return _decode_token(authorization[7:])


async def get_current_account(
    account: dict | None = Depends(get_optional_account),
) -> dict:
    if account is None:
        raise CustomException("请先登录", "401")
    return account


async def require_admin(account: dict = Depends(get_current_account)) -> dict:
    if account.get("role") != "管理员":
        raise CustomException("没有权限执行此操作", "403")
    return account