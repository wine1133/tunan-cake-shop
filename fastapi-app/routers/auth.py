from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from common.exception_handler import CustomException
from common.result import Result
from common.security import (
    create_token,
    get_current_account,
    hash_password,
    verify_password,
)
from models import Admin, User
from routers.utils import account_data

router = APIRouter(tags=["登录与账户"])


class LoginIn(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=100)
    role: str = "用户"


class RegisterIn(BaseModel):
    username: str = Field(min_length=2, max_length=30)
    password: str = Field(min_length=6, max_length=100)
    name: str | None = None


class PasswordIn(BaseModel):
    password: str
    newPassword: str = Field(min_length=6, max_length=100)


class ProfileIn(BaseModel):
    name: str | None = None
    avatar: str | None = None


@router.post("/login")
async def login(data: LoginIn):
    if data.role == "管理员":
        account = await Admin.get_or_none(username=data.username)
    else:
        account = await User.get_or_none(username=data.username)
    if account is None or not verify_password(data.password, account.password):
        raise CustomException("账号或密码错误")
    account_payload = account_data(account)
    token = create_token(
        account.id, account_payload["role"], account.name, account.username
    )
    return Result.success({**account_payload, "token": token}, "欢迎回来")


@router.post("/register")
async def register(data: RegisterIn):
    if await User.exists(username=data.username):
        raise CustomException("账号已存在，请更换一个")
    user = await User.create(
        username=data.username,
        password=hash_password(data.password),
        name=data.name or data.username,
        avatar=None,
        role="用户",
    )
    payload = account_data(user)
    return Result.success(
        {**payload, "token": create_token(user.id, "用户", user.name, user.username)},
        "注册成功",
    )


@router.get("/me")
async def get_me(account: dict = Depends(get_current_account)):
    if account["role"] == "管理员":
        item = await Admin.get_or_none(id=int(account["sub"]))
    else:
        item = await User.get_or_none(id=int(account["sub"]))
    if item is None:
        raise CustomException("账户不存在", "401")
    return Result.success(account_data(item))


@router.put("/profile")
async def update_profile(data: ProfileIn, account: dict = Depends(get_current_account)):
    model = Admin if account["role"] == "管理员" else User
    item = await model.get_or_none(id=int(account["sub"]))
    if item is None:
        raise CustomException("账户不存在", "401")
    if data.name is not None:
        if not data.name.strip():
            raise CustomException("昵称不能为空")
        item.name = data.name.strip()
    if data.avatar is not None:
        item.avatar = data.avatar
    await item.save()
    payload = account_data(item)
    payload["token"] = create_token(item.id, payload["role"], item.name, item.username)
    return Result.success(payload, "个人资料已更新")


@router.put("/updatePassword")
async def update_password(data: PasswordIn, account: dict = Depends(get_current_account)):
    model = Admin if account["role"] == "管理员" else User
    item = await model.get_or_none(id=int(account["sub"]))
    if item is None:
        raise CustomException("账户不存在", "401")
    if not verify_password(data.password, item.password):
        raise CustomException("原密码错误")
    if data.password == data.newPassword:
        raise CustomException("新密码不能与原密码相同")
    item.password = hash_password(data.newPassword)
    await item.save()
    return Result.success(None, "密码修改成功")