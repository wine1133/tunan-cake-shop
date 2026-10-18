from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from common.exception_handler import CustomException
from common.result import PageInfo, Result
from common.security import require_admin
from models import Notice
from routers.utils import notice_data, now_text

router = APIRouter(prefix="/notice", tags=["系统公告"])


class NoticeIn(BaseModel):
    id: int | None = None
    name: str | None = None
    content: str | None = None


@router.get("/selectPage")
async def select_page(
    name: str = "",
    page_num: int = Query(1, alias="pageNum", ge=1),
    page_size: int = Query(8, alias="pageSize", ge=1, le=100),
):
    query = Notice.all()
    if name:
        query = query.filter(name__contains=name)
    total = await query.count()
    rows = await query.order_by("-time", "-id").offset((page_num - 1) * page_size).limit(page_size)
    return Result.success(PageInfo(total=total, list=[notice_data(row) for row in rows]).model_dump())


@router.get("/selectAll")
async def select_all():
    rows = await Notice.all().order_by("-time", "-id").limit(20)
    return Result.success([notice_data(row) for row in rows])


@router.post("/add")
async def add(data: NoticeIn, _: dict = Depends(require_admin)):
    if not data.name or not data.name.strip():
        raise CustomException("请输入公告标题")
    if not data.content or not data.content.strip():
        raise CustomException("请输入公告内容")
    row = await Notice.create(name=data.name.strip(), content=data.content.strip(), time=now_text())
    return Result.success(notice_data(row), "公告已发布")


@router.put("/update")
async def update(data: NoticeIn, _: dict = Depends(require_admin)):
    if not data.id:
        raise CustomException("缺少公告ID")
    row = await Notice.get_or_none(id=data.id)
    if row is None:
        raise CustomException("公告不存在")
    if data.name is not None:
        row.name = data.name.strip()
    if data.content is not None:
        row.content = data.content.strip()
    await row.save()
    return Result.success(notice_data(row), "公告已更新")


@router.delete("/delete/{notice_id}")
async def delete(notice_id: int, _: dict = Depends(require_admin)):
    row = await Notice.get_or_none(id=notice_id)
    if row is None:
        raise CustomException("公告不存在")
    await row.delete()
    return Result.success(None, "公告已删除")