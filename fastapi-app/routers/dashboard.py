from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

from common.result import Result
from common.security import require_admin
from models import Category, Goods, Orders, User
from routers.utils import order_data

router = APIRouter(prefix="/dashboard", tags=["数据看板"])


@router.get("/stats")
async def stats(_: dict = Depends(require_admin)):
    users = await User.filter(role="用户").count()
    goods_count = await Goods.all().count()
    order_count = await Orders.all().count()
    month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    new_users = await User.filter(role="用户", created_at__gte=month_start).count()
    orders = await Orders.all().prefetch_related("goods", "user", "address").order_by("-created_at")
    revenue = sum(
        (order.goods.price or 0) * order.num
        for order in orders
        if order.goods and order.status != "已取消"
    )
    pending = sum(1 for order in orders if order.status in {"待制作", "制作中", "待取货"})
    avg_order = revenue / max(1, len([o for o in orders if o.status != "已取消"]))

    today = datetime.now().date()
    week = []
    for offset in range(6, -1, -1):
        day = today - timedelta(days=offset)
        value = sum(
            (order.goods.price or 0) * order.num
            for order in orders
            if order.created_at
            and order.created_at.date() == day
            and order.status != "已取消"
        )
        week.append({"date": day.strftime("%m/%d"), "label": "一二三四五六日"[day.weekday()], "value": round(value, 2)})

    category_sales: dict[int, float] = defaultdict(float)
    categories = await Category.all()
    goods_rows = await Goods.all()
    for goods in goods_rows:
        if goods.category_id:
            category_sales[goods.category_id] += (goods.price or 0) * (goods.sales or 0)
    total_category = sum(category_sales.values()) or 1
    category_distribution = [
        {
            "id": category.id,
            "name": category.name,
            "value": round(category_sales.get(category.id, 0), 2),
            "percent": round(category_sales.get(category.id, 0) / total_category * 100, 1),
        }
        for category in categories
    ]
    category_distribution.sort(key=lambda x: x["value"], reverse=True)

    low_stock = await Goods.filter(num__lte=8).order_by("num").limit(5)
    recent = [
        order_data(order, include_goods=True)
        for order in orders[:6]
    ]
    return Result.success(
        {
            "kpi": {
                "users": users,
                "goods": goods_count,
                "orders": order_count,
                "revenue": round(revenue, 2),
                "pending": pending,
                "newUsers": new_users,
                "avgOrder": round(avg_order, 2),
            },
            "week": week,
            "categoryDistribution": category_distribution[:6],
            "lowStock": [
                {"id": row.id, "name": row.name, "num": row.num, "img": row.img}
                for row in low_stock
            ],
            "recentOrders": recent,
        }
    )