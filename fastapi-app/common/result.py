from typing import Any

from pydantic import BaseModel


class PageInfo(BaseModel):
    total: int
    list: list[Any]


class Result:
    @staticmethod
    def success(data: Any = None, msg: str = "操作成功") -> dict:
        return {"code": "200", "msg": msg, "data": data}

    @staticmethod
    def error(msg: str, code: str = "500") -> dict:
        return {"code": code, "msg": msg, "data": None}