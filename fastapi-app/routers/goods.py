from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict, Field

from common.exception_handler import CustomException
from common.result import PageInfo, Result
from common.security import require_admin
from models import Category, Goods
from routers.utils import goods_data

router = APIRouter(prefix="/goods", tags=["蛋糕商品"])


class GoodsIn(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: int | None = None
    name: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    img: str | None = None
    price: float | None = Field(default=None, ge=0)
    num: int | None = Field(default=None, ge=0)
    unit: str | None = None
    category_id: int | None = Field(default=None, alias="categoryId")
    tag: str | None = None
    rating: float | None = None
    sales: int | None = None


@router.get("/selectPage")
async def select_page(
    name: str = "",
    category_id: int = Query(0, alias="categoryId"),
    featured: bool = False,
    page_num: int = Query(1, alias="pageNum", ge=1),
    page_size: int = Query(8, alias="pageSize", ge=1, le=100),
):
    query = Goods.all()
    if name:
        query = query.filter(name__contains=name)
    if category_id:
        query = query.filter(category_id=category_id)
    if featured:
        query = query.filter(tag__not_isnull=True).order_by("-sales").limit(6)
        rows = await query.prefetch_related("category")
        return Result.success(PageInfo(total=len(rows), list=[goods_data(row) for row in rows]).model_dump())
    total = await query.count()
    rows = (
        await query.order_by("-sales", "-created_at")
        .offset((page_num - 1) * page_size)
        .limit(page_size)
        .prefetch_related("category")
    )
    return Result.success(PageInfo(total=total, list=[goods_data(row) for row in rows]).model_dump())


@router.get("/{goods_id}")
async def detail(goods_id: int):
    row = await Goods.get_or_none(id=goods_id).prefetch_related("category")
    if row is None:
        raise CustomException("蛋糕不存在")
    return Result.success(goods_data(row))


@router.post("/add")
async def add(data: GoodsIn, _: dict = Depends(require_admin)):
    if not data.name or not data.name.strip():
        raise CustomException("请输入蛋糕名称")
    if not data.category_id:
        raise CustomException("请选择所属分类")
    if not await Category.exists(id=data.category_id):
        raise CustomException("分类不存在")
    row = await Goods.create(
        name=data.name.strip(),
        description=data.description or "",
        img=data.img or "/images/cake-celebration.jpg",
        price=data.price or 0,
        num=data.num or 0,
        unit=data.unit or "6寸",
        category_id=data.category_id,
        tag=data.tag,
        rating=data.rating or 4.9,
        sales=data.sales or 0,
    )
    return Result.success(goods_data(row), "蛋糕已上架")


@router.put("/update")
async def update(data: GoodsIn, _: dict = Depends(require_admin)):
    if not data.id:
        raise CustomException("缺少蛋糕ID")
    row = await Goods.get_or_none(id=data.id)
    if row is None:
        raise CustomException("蛋糕不存在")
    for attr in ("name", "description", "img", "price", "num", "unit", "tag", "rating", "sales"):
        value = getattr(data, attr)
        if value is not None:
            setattr(row, attr, value.strip() if isinstance(value, str) else value)
    if data.category_id is not None:
        if not await Category.exists(id=data.category_id):
            raise CustomException("分类不存在")
        row.category_id = data.category_id
    await row.save()
    return Result.success(goods_data(row), "蛋糕信息已更新")


@router.delete("/delete/{goods_id}")
async def delete(goods_id: int, _: dict = Depends(require_admin)):
    row = await Goods.get_or_none(id=goods_id)
    if row is None:
        raise CustomException("蛋糕不存在")
    await row.delete()
    return Result.success(None, "蛋糕已删除")