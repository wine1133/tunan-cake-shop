-- 兔南蛋糕零售店 · MySQL 8 初始化脚本
-- 默认体验账号：admin / admin123（管理员），user / user123（顾客）
SET NAMES utf8mb4;
CREATE DATABASE IF NOT EXISTS cake_shop DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cake_shop;
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `orders`;
DROP TABLE IF EXISTS `address`;
DROP TABLE IF EXISTS `goods`;
DROP TABLE IF EXISTS `category`;
DROP TABLE IF EXISTS `notice`;
DROP TABLE IF EXISTS `user`;
DROP TABLE IF EXISTS `admin`;

CREATE TABLE `admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `avatar` varchar(500) DEFAULT NULL,
  `role` varchar(20) NOT NULL DEFAULT '管理员',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_admin_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='管理员信息';

CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `avatar` varchar(500) DEFAULT NULL,
  `role` varchar(20) NOT NULL DEFAULT '用户',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户信息';

CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `icon` varchar(50) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_category_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='蛋糕分类';

CREATE TABLE `goods` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `img` varchar(500) DEFAULT NULL,
  `price` double NOT NULL DEFAULT 0,
  `num` int NOT NULL DEFAULT 0,
  `unit` varchar(50) NOT NULL DEFAULT '6寸',
  `tag` varchar(50) DEFAULT NULL,
  `rating` double NOT NULL DEFAULT 4.9,
  `sales` int NOT NULL DEFAULT 0,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `category_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_goods_category` (`category_id`),
  CONSTRAINT `fk_goods_category` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='蛋糕商品';

CREATE TABLE `address` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `address` varchar(500) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `is_default` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_address_user` (`user_id`),
  CONSTRAINT `fk_address_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='收货地址';

CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `num` int NOT NULL DEFAULT 1,
  `time` varchar(50) NOT NULL,
  `status` varchar(30) NOT NULL DEFAULT '待制作',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `address_id` int DEFAULT NULL,
  `goods_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_orders_address` (`address_id`),
  KEY `idx_orders_goods` (`goods_id`),
  KEY `idx_orders_user` (`user_id`),
  CONSTRAINT `fk_orders_address` FOREIGN KEY (`address_id`) REFERENCES `address` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_orders_goods` FOREIGN KEY (`goods_id`) REFERENCES `goods` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_orders_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单信息';

CREATE TABLE `notice` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `time` varchar(50) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统公告';
-- Seed data
INSERT INTO `admin` (`id`, `username`, `password`, `name`, `avatar`, `role`, `created_at`) VALUES
(1, 'admin', 'pbkdf2_sha256$260000$trDF7Ik-gmcc6ve8bZhycg==$OfGlLJKC23vm8ZnTqEcqYvZGKsxWGcdDgrWSAVKnGps=', '兔南主理人', NULL, '管理员', '2026-10-17 23:06:57.068642');

INSERT INTO `user` (`id`, `username`, `password`, `name`, `avatar`, `role`, `created_at`) VALUES
(1, 'user', 'pbkdf2_sha256$260000$qAO77U3FJHfRSFDlJAE7TA==$Sl1FD1EDJQDRMXrofNB5o1VzVLq2dKmhqaJdqO-Safc=', '林小满', NULL, '用户', '2026-10-17 23:06:57.160679'),
(2, 'chenzhixia', 'pbkdf2_sha256$260000$DzatqJNkeIP_8Fm4BfVmUA==$INZanahE2rTu1Q7aoq_7Kt0mhTJhDRw1tzTLJGy2bo0=', '陈知夏', NULL, '用户', '2026-10-17 23:06:57.252881'),
(3, 'suyue', 'pbkdf2_sha256$260000$BShmmryfQ4tQKkW4aorvMQ==$40lF2w5jlEYUSzV5q_QfLNQ-rsMNk7XBjrmETu7JT5o=', '苏月', NULL, '用户', '2026-10-17 23:06:57.343432'),
(4, 'zhouyu', 'pbkdf2_sha256$260000$_vlz0bj2v7q6NhMxXB0KlA==$Z9RQqbuWN_GcvQK4M-xQCzvl3UzgB6DeiZI2-d_2QGc=', '周予', NULL, '用户', '2026-10-17 23:06:57.432907');

INSERT INTO `category` (`id`, `name`, `description`, `icon`, `created_at`) VALUES
(1, '经典奶油', '轻盈如云，入口即化的温柔', 'cream', '2026-10-17 23:06:57.434892'),
(2, '法式慕斯', '细腻层叠，法式甜点的浪漫表达', 'mousse', '2026-10-17 23:06:57.436892'),
(3, '浓情巧克力', '醇厚可可，给味蕾一场深邃旅行', 'chocolate', '2026-10-17 23:06:57.436892'),
(4, '轻乳酪', '芝士与奶香恰到好处的平衡', 'cheese', '2026-10-17 23:06:57.439402'),
(5, '节日限定', '为值得纪念的日子，特别制作', 'celebration', '2026-10-17 23:06:57.441404'),
(6, '午后甜点', '一人食的松弛与小小犒赏', 'teatime', '2026-10-17 23:06:57.443403');

INSERT INTO `goods` (`id`, `name`, `description`, `img`, `price`, `num`, `unit`, `tag`, `rating`, `sales`, `created_at`, `category_id`) VALUES
(1, '云朵草莓蛋糕', '北海道奶油、香草戚风与当季红颜草莓，轻盈得像一朵甜云。', '/images/cake-strawberry.jpg', 268.0, 18, '6寸', '人气 TOP1', 4.9, 328, '2026-10-17 23:06:57.445402', 1),
(2, '馥郁黑森林', '70% 法芙娜黑巧、酒渍樱桃与可可海绵，微苦之后是绵长回甘。', '/images/cake-chocolate.jpg', 298.0, 12, '6寸', '主厨推荐', 4.8, 256, '2026-10-17 23:06:57.448928', 3),
(3, '白桃乌龙慕斯', '白桃果茸与冷萃乌龙茶香交叠，清甜不腻的秋日新作。', '/images/cake-berry.jpg', 328.0, 9, '6寸', '秋日新作', 4.9, 198, '2026-10-17 23:06:57.449964', 2),
(4, '抹茶青岚', '宇治抹茶与白巧甘纳许，茶香清冽，尾韵温柔。', '/images/cake-matcha.jpg', 288.0, 15, '6寸', '清新回甘', 4.8, 176, '2026-10-17 23:06:57.451934', 2),
(5, '海盐芝士', '法国海盐遇见浓郁芝士，酥脆饼干底托住恰到好处的咸甜。', '/images/cake-vanilla.jpg', 218.0, 20, '6寸', '经典之选', 4.7, 289, '2026-10-17 23:06:57.452956', 4),
(6, '焦糖榛果', '慢熬海盐焦糖、烘烤榛子与柔软可可胚，醇厚而不甜腻。', '/images/cake-chocolate.jpg', 258.0, 7, '6寸', '醇厚不腻', 4.8, 143, '2026-10-17 23:06:57.453934', 3),
(7, '香槟玫瑰', '玫瑰慕斯包裹香槟梨夹心，为纪念日留下一抹优雅香气。', '/images/cake-berry.jpg', 368.0, 6, '8寸', '纪念日', 4.9, 96, '2026-10-17 23:06:57.455935', 5),
(8, '柠檬轻芝士', '新鲜柠檬皮屑与 Kiri 芝士，清爽轻盈，适合一个人的下午茶。', '/images/cake-lemon.jpg', 198.0, 22, '4寸', '下午茶', 4.7, 221, '2026-10-17 23:06:57.456934', 4),
(9, '花园纸杯组', '六枚装迷你花园蛋糕，三种口味，适合分享每一个小确幸。', '/images/cake-cupcake.jpg', 128.0, 28, '6枚', '分享装', 4.8, 315, '2026-10-17 23:06:57.459176', 6),
(10, '生日星光', '可定制祝福语与蜡烛，以星光为灵感，为重要时刻加冕。', '/images/cake-celebration.jpg', 398.0, 5, '8寸', '仪式感', 4.9, 187, '2026-10-17 23:06:57.460814', 5);

INSERT INTO `address` (`id`, `name`, `address`, `phone`, `is_default`, `created_at`, `user_id`) VALUES
(1, '林小满', '上海市徐汇区安福路 288 号 5 栋 1202 室', '13800138000', 1, '2026-10-17 23:06:57.463086', 1);

INSERT INTO `orders` (`id`, `num`, `time`, `status`, `created_at`, `address_id`, `goods_id`, `user_id`) VALUES
(1, 1, '2026-10-18 05:06', '制作中', '2026-10-18 05:06:57.470623', 1, 1, 1),
(2, 1, '2026-10-17 05:06', '待取货', '2026-10-17 05:06:57.474602', 1, 3, 1),
(3, 2, '2026-10-16 05:06', '已完成', '2026-10-16 05:06:57.477620', 1, 5, 1),
(4, 1, '2026-10-15 05:06', '已完成', '2026-10-15 05:06:57.480150', 1, 2, 2),
(5, 1, '2026-10-13 05:06', '已完成', '2026-10-13 05:06:57.483329', 1, 4, 3),
(6, 2, '2026-10-18 05:06', '待制作', '2026-10-18 05:06:57.486405', 1, 9, 4),
(7, 1, '2026-10-12 05:06', '已完成', '2026-10-12 05:06:57.489575', 1, 10, 2);

INSERT INTO `notice` (`id`, `name`, `content`, `time`, `created_at`) VALUES
(1, '秋日限定 · 白桃乌龙慕斯上新', '即日起至 10 月 31 日，预订秋日限定系列享双倍会员积分，每日限量 20 份。', '2026-10-08 10:30', '2026-10-17 23:06:57.465123'),
(2, '关于蛋糕预订与配送时间', '所有蛋糕均为接单后新鲜制作，请至少提前 24 小时预订。上海市内支持冷链配送。', '2026-10-06 14:20', '2026-10-17 23:06:57.466096'),
(3, '兔南会员日 · 每周三', '每周三会员下单享 9 折，生日当月更可领取专属蜡烛与贺卡。', '2026-10-01 09:00', '2026-10-17 23:06:57.467094');

SET FOREIGN_KEY_CHECKS = 1;
