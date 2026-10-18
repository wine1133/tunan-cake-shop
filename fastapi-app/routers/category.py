from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from common.exception_handler import CustomException
from common.result import PageInfo, Result
from common.security import require_admin
from models import Category, Goods
from routers.utils import category_data

router = APIRouter(prefix="/category", tags=["蛋糕分类"])


class CategoryIn(BaseModel):
    id: int | None = None
    name: str | None = None
    description: str | None = None
    icon: str | None = None


@router.get("/selectAll")
async def select_all():
    rows = await Category.all().order_by("id")
    return Result.success([category_data(row) for row in rows])


@router.get("/selectPage")
async def select_page(
    name: str = "",
    page_num: int = Query(1, alias="pageNum", ge=1),
    page_size: int = Query(8, alias="pageSize", ge=1, le=100),
):
    query = Category.all()
    if name:
        query = query.filter(name__contains=name)
    total = await query.count()
    rows = await query.order_by("id").offset((page_num - 1) * page_size).limit(page_size)
    return Result.success(PageInfo(total=total, list=[category_data(row) for row in rows]).model_dump())


@router.post("/add")
async def add(data: CategoryIn, _: dict = Depends(require_admin)):
    if not data.name or not data.name.strip():
        raise CustomException("请输入分类名称")
    if await Category.exists(name=data.name.strip()):
        raise CustomException("分类名称已存在")
    row = await Category.create(
        name=data.name.strip(),
        description=data.description,
        icon=data.icon,
    )
    return Result.success(category_data(row), "分类已创建")


@router.put("/update")
async def update(data: CategoryIn, _: dict = Depends(require_admin)):
    if not data.id:
        raise CustomException("缺少分类ID")
    row = await Category.get_or_none(id=data.id)
    if row is None:
        raise CustomException("分类不存在")
    if data.name is not None:
        if not data.name.strip():
            raise CustomException("分类名称不能为空")
        duplicate = await Category.filter(name=data.name.strip()).exclude(id=data.id).first()
        if duplicate:
            raise CustomException("分类名称已存在")
        row.name = data.name.strip()
    if data.description is not None:
        row.description = data.description
    if data.icon is not None:
        row.icon = data.icon
    await row.save()
    return Result.success(category_data(row), "分类已更新")


@router.delete("/delete/{category_id}")
async def delete(category_id: int, _: dict = Depends(require_admin)):
    row = await Category.get_or_none(id=category_id)
    if row is None:
        raise CustomException("分类不存在")
    if await Goods.exists(category_id=category_id):
        raise CustomException("该分类下仍有蛋糕，暂时无法删除")
    await row.delete()
    return Result.success(None, "分类已删除")