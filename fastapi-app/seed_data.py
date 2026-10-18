from datetime import datetime, timedelta

from common.security import hash_password
from models import Address, Admin, Category, Goods, Notice, Orders, User


async def seed_database():
    if not await Admin.exists(username="admin"):
        await Admin.create(
            username="admin",
            password=hash_password("admin123"),
            name="兔南主理人",
            avatar=None,
            role="管理员",
        )

    if not await User.exists(username="user"):
        user = await User.create(
            username="user",
            password=hash_password("user123"),
            name="林小满",
            avatar=None,
            role="用户",
        )
    else:
        user = await User.get(username="user")

    demo_users = [
        ("chenzhixia", "陈知夏", "13800138021"),
        ("suyue", "苏月", "13900139032"),
        ("zhouyu", "周予", "13600136043"),
    ]
    if await User.filter(role="用户").count() < 4:
        for username, name, _ in demo_users:
            if not await User.exists(username=username):
                await User.create(
                    username=username,
                    password=hash_password("123456"),
                    name=name,
                    avatar=None,
                    role="用户",
                )

    if not await Category.exists():
        categories = [
            ("经典奶油", "轻盈如云，入口即化的温柔", "cream"),
            ("法式慕斯", "细腻层叠，法式甜点的浪漫表达", "mousse"),
            ("浓情巧克力", "醇厚可可，给味蕾一场深邃旅行", "chocolate"),
            ("轻乳酪", "芝士与奶香恰到好处的平衡", "cheese"),
            ("节日限定", "为值得纪念的日子，特别制作", "celebration"),
            ("午后甜点", "一人食的松弛与小小犒赏", "teatime"),
        ]
        for name, description, icon in categories:
            await Category.create(name=name, description=description, icon=icon)

    categories = await Category.all().order_by("id")
    category_map = {item.name: item for item in categories}

    if not await Goods.exists():
        goods = [
            ("云朵草莓蛋糕", "北海道奶油、香草戚风与当季红颜草莓，轻盈得像一朵甜云。", "/images/cake-strawberry.jpg", 268, 18, "6寸", "经典奶油", "人气 TOP1", 4.9, 328),
            ("馥郁黑森林", "70% 法芙娜黑巧、酒渍樱桃与可可海绵，微苦之后是绵长回甘。", "/images/cake-chocolate.jpg", 298, 12, "6寸", "浓情巧克力", "主厨推荐", 4.8, 256),
            ("白桃乌龙慕斯", "白桃果茸与冷萃乌龙茶香交叠，清甜不腻的秋日新作。", "/images/cake-berry.jpg", 328, 9, "6寸", "法式慕斯", "秋日新作", 4.9, 198),
            ("抹茶青岚", "宇治抹茶与白巧甘纳许，茶香清冽，尾韵温柔。", "/images/cake-matcha.jpg", 288, 15, "6寸", "法式慕斯", "清新回甘", 4.8, 176),
            ("海盐芝士", "法国海盐遇见浓郁芝士，酥脆饼干底托住恰到好处的咸甜。", "/images/cake-vanilla.jpg", 218, 20, "6寸", "轻乳酪", "经典之选", 4.7, 289),
            ("焦糖榛果", "慢熬海盐焦糖、烘烤榛子与柔软可可胚，醇厚而不甜腻。", "/images/cake-chocolate.jpg", 258, 7, "6寸", "浓情巧克力", "醇厚不腻", 4.8, 143),
            ("香槟玫瑰", "玫瑰慕斯包裹香槟梨夹心，为纪念日留下一抹优雅香气。", "/images/cake-berry.jpg", 368, 6, "8寸", "节日限定", "纪念日", 4.9, 96),
            ("柠檬轻芝士", "新鲜柠檬皮屑与 Kiri 芝士，清爽轻盈，适合一个人的下午茶。", "/images/cake-lemon.jpg", 198, 22, "4寸", "轻乳酪", "下午茶", 4.7, 221),
            ("花园纸杯组", "六枚装迷你花园蛋糕，三种口味，适合分享每一个小确幸。", "/images/cake-cupcake.jpg", 128, 28, "6枚", "午后甜点", "分享装", 4.8, 315),
            ("生日星光", "可定制祝福语与蜡烛，以星光为灵感，为重要时刻加冕。", "/images/cake-celebration.jpg", 398, 5, "8寸", "节日限定", "仪式感", 4.9, 187),
        ]
        for name, desc, img, price, num, unit, category, tag, rating, sales in goods:
            await Goods.create(
                name=name,
                description=desc,
                img=img,
                price=price,
                num=num,
                unit=unit,
                category_id=category_map[category].id,
                tag=tag,
                rating=rating,
                sales=sales,
            )

    if not await Address.exists(user_id=user.id):
        address = await Address.create(
            user_id=user.id,
            name="林小满",
            address="上海市徐汇区安福路 288 号 5 栋 1202 室",
            phone="13800138000",
            is_default=True,
        )
    else:
        address = await Address.filter(user_id=user.id).order_by("-is_default").first()

    if not await Notice.exists():
        notices = [
            ("秋日限定 · 白桃乌龙慕斯上新", "即日起至 10 月 31 日，预订秋日限定系列享双倍会员积分，每日限量 20 份。", "2026-10-08 10:30"),
            ("关于蛋糕预订与配送时间", "所有蛋糕均为接单后新鲜制作，请至少提前 24 小时预订。上海市内支持冷链配送。", "2026-10-06 14:20"),
            ("兔南会员日 · 每周三", "每周三会员下单享 9 折，生日当月更可领取专属蜡烛与贺卡。", "2026-10-01 09:00"),
        ]
        for name, content, time in notices:
            await Notice.create(name=name, content=content, time=time)

    if not await Orders.exists() and address:
        goods = await Goods.all().order_by("id")
        users = await User.filter(role="用户").order_by("id")
        if len(goods) >= 3 and users:
            order_specs = [
                (goods[0], users[0], address, 1, 0, "制作中"),
                (goods[2], users[0], address, 1, 1, "待取货"),
                (goods[4], users[0], address, 2, 2, "已完成"),
                (goods[1], users[1] if len(users) > 1 else users[0], address, 1, 3, "已完成"),
                (goods[3], users[2] if len(users) > 2 else users[0], address, 1, 5, "已完成"),
                (goods[8], users[3] if len(users) > 3 else users[0], address, 2, 0, "待制作"),
                (goods[9], users[1] if len(users) > 1 else users[0], address, 1, 6, "已完成"),
            ]
            for goods_row, user_row, address_row, num, days_ago, status in order_specs:
                created = datetime.now() - timedelta(days=days_ago, hours=2)
                order = await Orders.create(
                    num=num,
                    user_id=user_row.id,
                    goods_id=goods_row.id,
                    address_id=address_row.id,
                    time=created.strftime("%Y-%m-%d %H:%M"),
                    status=status,
                )
                await Orders.filter(id=order.id).update(created_at=created)