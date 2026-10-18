from datetime import datetime

from tortoise import fields
from tortoise.models import Model


class Admin(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)
    avatar = fields.CharField(max_length=500, null=True)
    role = fields.CharField(max_length=20, default="管理员")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "admin"


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    name = fields.CharField(max_length=255)
    avatar = fields.CharField(max_length=500, null=True)
    role = fields.CharField(max_length=20, default="用户")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "user"


class Category(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    description = fields.CharField(max_length=255, null=True)
    icon = fields.CharField(max_length=50, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "category"


class Goods(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.CharField(max_length=500, null=True)
    img = fields.CharField(max_length=500, null=True)
    price = fields.FloatField(default=0)
    num = fields.IntField(default=0)
    unit = fields.CharField(max_length=50, default="6寸")
    category: fields.ForeignKeyNullableRelation[Category] = fields.ForeignKeyField(
        "models.Category", related_name="goods", null=True
    )
    tag = fields.CharField(max_length=50, null=True)
    rating = fields.FloatField(default=4.9)
    sales = fields.IntField(default=0)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "goods"


class Address(Model):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyNullableRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="addresses", null=True
    )
    name = fields.CharField(max_length=255)
    address = fields.CharField(max_length=500)
    phone = fields.CharField(max_length=50)
    is_default = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "address"


class Orders(Model):
    id = fields.IntField(pk=True)
    num = fields.IntField(default=1)
    user: fields.ForeignKeyNullableRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="orders", null=True
    )
    goods: fields.ForeignKeyNullableRelation[Goods] = fields.ForeignKeyField(
        "models.Goods", related_name="orders", null=True
    )
    address: fields.ForeignKeyNullableRelation[Address] = fields.ForeignKeyField(
        "models.Address", related_name="orders", null=True
    )
    time = fields.CharField(max_length=50)
    status = fields.CharField(max_length=30, default="待制作")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "orders"


class Notice(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    content = fields.TextField()
    time = fields.CharField(max_length=50, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "notice"