from fastapi import Request
from fastapi.responses import JSONResponse


class CustomException(Exception):
    def __init__(self, message: str, code: str = "500"):
        self.message = message
        self.code = code
        super().__init__(message)


async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=200,
        content={"code": exc.code, "msg": exc.message, "data": None},
    )


async def validation_exception_handler(request: Request, exc):
    errors = getattr(exc, "errors", lambda: [])()
    message = errors[0].get("msg", "请求参数不正确") if errors else "请求参数不正确"
    if message.startswith("Value error, "):
        message = message[13:]
    return JSONResponse(
        status_code=200,
        content={"code": "400", "msg": message, "data": None},
    )