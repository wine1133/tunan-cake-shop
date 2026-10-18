from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict, Field

from common.exception_handler import CustomException
from common.result import PageInfo, Result
from common.security import get_current_account
from models import Address, User
from routers.utils import address_data

router = APIRouter(prefix="/address", tags=["收货地址"])


class AddressIn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: int | None = None
    user_id: int | None = Field(default=None, alias="userId")
    name: str | None = Field(default=None, max_length=50)
    address: str | None = Field(default=None, max_length=500)
    phone: str | None = Field(default=None, max_length=30)
    is_default: bool | None = Field(default=None, alias="isDefault")


@router.get("/selectPage")
async def select_page(
    address: str = "",
    user_id: int = Query(0, alias="userId"),
    page_num: int = Query(1, alias="pageNum", ge=1),
    page_size: int = Query(8, alias="pageSize", ge=1, le=100),
    account: dict = Depends(get_current_account),
):
    query = Address.all()
    if account["role"] != "管理员":
        query = query.filter(user_id=int(account["sub"]))
    elif user_id:
        query = query.filter(user_id=user_id)
    if address:
        query = query.filter(address__contains=address)
    total = await query.count()
    rows = (
        await query.order_by("-is_default", "-created_at")
        .offset((page_num - 1) * page_size)
        .limit(page_size)
        .prefetch_related("user")
    )
    return Result.success(PageInfo(total=total, list=[address_data(row) for row in rows]).model_dump())


@router.get("/selectAll")
async def select_all(account: dict = Depends(get_current_account)):
    query = Address.all()
    if account["role"] != "管理员":
        query = query.filter(user_id=int(account["sub"]))
    rows = await query.order_by("-is_default", "-created_at")
    return Result.success([address_data(row) for row in rows])


@router.post("/add")
async def add(data: AddressIn, account: dict = Depends(get_current_account)):
    if not data.name or not data.name.strip():
        raise CustomException("请输入收货人")
    if not data.address or not data.address.strip():
        raise CustomException("请输入收货地址")
    if not data.phone or not data.phone.strip():
        raise CustomException("请输入联系方式")
    user_id = data.user_id
    if account["role"] != "管理员":
        user_id = int(account["sub"])
    if not user_id or not await User.exists(id=user_id):
        raise CustomException("用户不存在")
    has_address = await Address.exists(user_id=user_id)
    is_default = data.is_default if data.is_default is not None else not has_address
    if is_default:
        await Address.filter(user_id=user_id).update(is_default=False)
    row = await Address.create(
        user_id=user_id,
        name=data.name.strip(),
        address=data.address.strip(),
        phone=data.phone.strip(),
        is_default=is_default,
    )
    return Result.success(address_data(row), "地址已保存")


@router.put("/update")
async def update(data: AddressIn, account: dict = Depends(get_current_account)):
    if not data.id:
        raise CustomException("缺少地址ID")
    row = await Address.get_or_none(id=data.id)
    if row is None:
        raise CustomException("地址不存在")
    if account["role"] != "管理员" and row.user_id != int(account["sub"]):
        raise CustomException("无权修改该地址", "403")
    if data.name is not None:
        row.name = data.name.strip()
    if data.address is not None:
        row.address = data.address.strip()
    if data.phone is not None:
        row.phone = data.phone.strip()
    if data.is_default is not None:
        if data.is_default:
            await Address.filter(user_id=row.user_id).update(is_default=False)
        row.is_default = data.is_default
    await row.save()
    return Result.success(address_data(row), "地址已更新")


@router.delete("/delete/{address_id}")
async def delete(address_id: int, account: dict = Depends(get_current_account)):
    row = await Address.get_or_none(id=address_id)
    if row is None:
        raise CustomException("地址不存在")
    if account["role"] != "管理员" and row.user_id != int(account["sub"]):
        raise CustomException("无权删除该地址", "403")
    await row.delete()
    return Result.success(None, "地址已删除")