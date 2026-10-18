from datetime import datetime

from models import Address, Admin, Category, Goods, Notice, Orders, User


def _related(value):
    """Tortoise returns a lazy QuerySet for non-prefetched foreign keys."""
    return value if value is not None and hasattr(value, "id") else None


def account_data(account) -> dict:
    role = "管理员" if isinstance(account, Admin) else "用户"
    return {
        "id": account.id,
        "username": account.username,
        "name": account.name,
        "avatar": account.avatar,
        "role": role,
    }


def user_data(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "avatar": user.avatar,
        "role": user.role,
        "createdAt": user.created_at.strftime("%Y-%m-%d") if user.created_at else None,
    }


def category_data(category: Category) -> dict:
    return {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "icon": category.icon,
    }


def goods_data(goods: Goods, category: Category | None = None) -> dict:
    category = _related(category) or _related(getattr(goods, "category", None))
    return {
        "id": goods.id,
        "name": goods.name,
        "description": goods.description,
        "img": goods.img,
        "price": round(goods.price or 0, 2),
        "num": goods.num,
        "unit": goods.unit,
        "categoryId": category.id if category else goods.category_id,
        "categoryName": category.name if category else "未分类",
        "tag": goods.tag,
        "rating": goods.rating,
        "sales": goods.sales,
    }


def address_data(address: Address, user: User | None = None) -> dict:
    user = _related(user) or _related(getattr(address, "user", None))
    return {
        "id": address.id,
        "userId": user.id if user else address.user_id,
        "userName": user.name if user else None,
        "name": address.name,
        "address": address.address,
        "phone": address.phone,
        "isDefault": address.is_default,
    }


def order_data(order: Orders, include_goods: bool = True) -> dict:
    goods = _related(getattr(order, "goods", None))
    address = _related(getattr(order, "address", None))
    user = _related(getattr(order, "user", None))
    result = {
        "id": order.id,
        "num": order.num,
        "time": order.time,
        "status": order.status,
        "userId": user.id if user else order.user_id,
        "userName": user.name if user else None,
        "goodsId": goods.id if goods else order.goods_id,
        "addressId": address.id if address else order.address_id,
        "aName": address.name if address else None,
        "aAddress": address.address if address else None,
        "aPhone": address.phone if address else None,
    }
    if include_goods:
        result.update(
            {
                "goodsName": goods.name if goods else None,
                "goodsUnit": goods.unit if goods else None,
                "goodsImg": goods.img if goods else None,
                "goodsPrice": round(goods.price or 0, 2) if goods else None,
                "total": round((goods.price or 0) * order.num, 2) if goods else None,
            }
        )
    return result


def notice_data(notice: Notice) -> dict:
    return {
        "id": notice.id,
        "name": notice.name,
        "content": notice.content,
        "time": notice.time,
    }


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")