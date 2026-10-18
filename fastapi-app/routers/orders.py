from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict, Field
from tortoise.transactions import in_transaction

from common.exception_handler import CustomException
from common.result import PageInfo, Result
from common.security import get_current_account, require_admin
from models import Address, Goods, Orders
from routers.utils import now_text, order_data

router = APIRouter(prefix="/orders", tags=["订单管理"])


class OrderIn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: int | None = None
    num: int | None = Field(default=1, ge=1, le=99)
    user_id: int | None = Field(default=None, alias="userId")
    goods_id: int | None = Field(default=None, alias="goodsId")
    address_id: int | None = Field(default=None, alias="addressId")


class StatusIn(BaseModel):
    status: str


@router.get("/selectPage")
async def select_page(
    goods_name: str = Query("", alias="goodsName"),
    user_id: int = Query(0, alias="userId"),
    status: str = "",
    page_num: int = Query(1, alias="pageNum", ge=1),
    page_size: int = Query(8, alias="pageSize", ge=1, le=100),
    account: dict = Depends(get_current_account),
):
    query = Orders.all()
    if account["role"] != "管理员":
        query = query.filter(user_id=int(account["sub"]))
    elif user_id:
        query = query.filter(user_id=user_id)
    if status:
        query = query.filter(status=status)
    if goods_name:
        query = query.filter(goods__name__contains=goods_name)
    total = await query.count()
    rows = (
        await query.order_by("-created_at")
        .offset((page_num - 1) * page_size)
        .limit(page_size)
        .prefetch_related("address", "user", "goods")
    )
    return Result.success(PageInfo(total=total, list=[order_data(row) for row in rows]).model_dump())


@router.post("/add")
async def add(data: OrderIn, account: dict = Depends(get_current_account)):
    if not data.goods_id:
        raise CustomException("请选择蛋糕")
    if not data.address_id:
        raise CustomException("请选择收货地址")
    user_id = data.user_id if account["role"] == "管理员" and data.user_id else int(account["sub"])
    address = await Address.get_or_none(id=data.address_id, user_id=user_id)
    if address is None:
        raise CustomException("收货地址不存在")
    quantity = data.num or 1
    async with in_transaction():
        goods = await Goods.select_for_update().get_or_none(id=data.goods_id)
        if goods is None:
            raise CustomException("蛋糕不存在")
        if (goods.num or 0) < quantity:
            raise CustomException(f"库存不足，当前仅剩 {goods.num or 0} 份")
        order = await Orders.create(
            num=quantity,
            user_id=user_id,
            goods_id=goods.id,
            address_id=address.id,
            time=now_text(),
            status="待制作",
        )
        goods.num = (goods.num or 0) - quantity
        goods.sales = (goods.sales or 0) + quantity
        await goods.save()
    order = await Orders.get(id=order.id).prefetch_related("address", "user", "goods")
    return Result.success(order_data(order), "预订成功，甜蜜正在准备中")


@router.put("/status/{order_id}")
async def update_status(
    order_id: int, data: StatusIn, _: dict = Depends(require_admin)
):
    if data.status not in {"待制作", "制作中", "待取货", "已完成", "已取消"}:
        raise CustomException("订单状态不正确")
    order = await Orders.get_or_none(id=order_id)
    if order is None:
        raise CustomException("订单不存在")
    order.status = data.status
    await order.save()
    return Result.success(None, "订单状态已更新")


@router.delete("/delete/{order_id}")
async def delete(order_id: int, account: dict = Depends(get_current_account)):
    order = await Orders.get_or_none(id=order_id)
    if order is None:
        raise CustomException("订单不存在")
    if account["role"] != "管理员" and order.user_id != int(account["sub"]):
        raise CustomException("无权删除该订单", "403")
    async with in_transaction():
        goods = await Goods.get_or_none(id=order.goods_id)
        if goods:
            goods.num = (goods.num or 0) + order.num
            goods.sales = max(0, (goods.sales or 0) - order.num)
            await goods.save()
        await order.delete()
    return Result.success(None, "订单已删除")