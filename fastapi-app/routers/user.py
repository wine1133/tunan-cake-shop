from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict, Field

from common.exception_handler import CustomException
from common.result import PageInfo, Result
from common.security import hash_password, require_admin
from models import User
from routers.utils import user_data

router = APIRouter(prefix="/user", tags=["用户管理"])


class UserIn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: int | None = None
    username: str | None = Field(default=None, max_length=30)
    name: str | None = Field(default=None, max_length=50)
    avatar: str | None = None
    password: str | None = None


@router.get("/selectPage")
async def select_page(
    name: str = "",
    page_num: int = Query(1, alias="pageNum", ge=1),
    page_size: int = Query(8, alias="pageSize", ge=1, le=100),
    _: dict = Depends(require_admin),
):
    query = User.filter(role="用户")
    if name:
        query = query.filter(name__contains=name) | User.filter(
            role="用户", username__contains=name
        )
    total = await query.count()
    rows = await query.order_by("-created_at").offset((page_num - 1) * page_size).limit(page_size)
    return Result.success(PageInfo(total=total, list=[user_data(row) for row in rows]).model_dump())


@router.post("/add")
async def add(data: UserIn, _: dict = Depends(require_admin)):
    if not data.username or not data.username.strip():
        raise CustomException("请输入账号")
    if await User.exists(username=data.username.strip()):
        raise CustomException("账号重复")
    user = await User.create(
        username=data.username.strip(),
        name=(data.name or data.username).strip(),
        password=hash_password(data.password or "123456"),
        avatar=data.avatar,
        role="用户",
    )
    return Result.success(user_data(user), "用户已创建")


@router.put("/update")
async def update(data: UserIn, _: dict = Depends(require_admin)):
    if not data.id:
        raise CustomException("缺少用户ID")
    user = await User.get_or_none(id=data.id)
    if user is None:
        raise CustomException("用户不存在")
    if data.name is not None:
        user.name = data.name.strip()
    if data.avatar is not None:
        user.avatar = data.avatar
    if data.password:
        if len(data.password) < 6:
            raise CustomException("密码至少需要 6 位")
        user.password = hash_password(data.password)
    await user.save()
    return Result.success(user_data(user), "用户信息已更新")


@router.delete("/delete/{user_id}")
async def delete(user_id: int, _: dict = Depends(require_admin)):
    user = await User.get_or_none(id=user_id)
    if user is None:
        raise CustomException("用户不存在")
    await user.delete()
    return Result.success(None, "用户已删除")