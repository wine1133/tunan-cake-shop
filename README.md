# 兔南蛋糕零售店

一套完整、可直接运行的中文蛋糕零售店系统，包含 **顾客预订端 + 店铺管理后台 + FastAPI API 服务**。界面以奶油白、可可棕与玫瑰金为主视觉，围绕「手作、季节、仪式感」构建品牌体验。

![兔南蛋糕零售店](vue-app/public/images/hero-cake.jpg)

## 功能一览

### 顾客端
- 品牌首页：视频轮播（支持声音开关）、分类导航、人气蛋糕、品牌故事、顾客口碑、公告播报
- 全部蛋糕：分类筛选、关键词搜索、人气/价格排序、分页
- 在线预订：蛋糕详情、数量选择、收货地址选择、库存实时校验
- 我的订单：订单状态跟进、订单金额统计、取消/删除记录
- 收货地址：新增、编辑、删除、设为默认地址
- 个人中心：头像上传、昵称修改、密码修改
- 登录 / 注册 / 角色自动识别

### 管理后台
- 数据总览：营业额、订单、会员、商品、近 7 日销售、品类占比、库存提醒、最近订单
- 蛋糕管理：新增、编辑、上下架、库存、价格、分类、图片上传、标签与评分
- 分类管理：分类创建、编辑、删除保护（分类下有商品时禁止删除）
- 订单管理：检索、筛选、详情抽屉、状态流转、删除并自动回补库存
- 用户管理：新增、编辑、头像上传、密码重置、删除
- 收货地址：全量查询与删除
- 系统公告：发布、编辑、删除，并同步到店铺首页

### 工程能力
- JWT 登录凭证 + PBKDF2-SHA256 密码哈希
- 管理端/顾客端接口权限隔离
- SQLite 零配置运行；MySQL 8 一行切换
- Tortoise ORM 自动建表与种子数据
- 页面级懒加载、响应式布局、移动端适配
- 统一业务返回结构 `{ code, msg, data }`

## 技术栈

| 模块 | 技术 |
| --- | --- |
| 后端 | Python 3.12、FastAPI、Tortoise ORM、PyJWT、Uvicorn |
| 数据库 | SQLite（默认） / MySQL 8 |
| 前端 | Vue 3、Vite、Vue Router、Element Plus、Axios |
| 设计 | 原生 CSS 设计系统、响应式布局、无第三方图表依赖 |

## 目录结构

```text
蛋糕零售店/
├─ fastapi-app/                 # FastAPI 后端
│  ├─ common/                   # 统一响应、异常、JWT、密码哈希
│  ├─ routers/                  # 登录、用户、分类、商品、地址、订单、公告、看板
│  ├─ static/uploads/           # 上传图片
│  ├─ data/                     # SQLite 数据库（自动生成）
│  ├─ models.py                 # Tortoise 数据模型
│  ├─ seed_data.py              # 初始化演示数据
│  ├─ main.py                   # 应用入口
│  ├─ settings.py               # 环境配置
│  └─ requirements.txt
├─ vue-app/                     # Vue 3 前端
│  ├─ public/images/            # 蛋糕产品图与品牌图
│  └─ src/
│     ├─ components/            # 布局、品牌、商品卡、预订弹窗
│     ├─ views/                 # 顾客端页面
│     ├─ views/admin/           # 管理后台页面
│     ├─ router/
│     ├─ utils/
│     └─ styles/global.css      # 全局设计系统
├─ sql/cake_shop.sql            # MySQL 8 建表 + 演示数据
└─ README.md
```

## 快速启动

### 1. 启动后端（默认 SQLite，无需安装数据库）

```powershell
cd fastapi-app
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

首次启动会自动创建 `fastapi-app/data/cake_shop.db` 并写入演示数据。

### 2. 启动前端

```powershell
cd vue-app
npm install
npm run dev
```

浏览器打开：<http://127.0.0.1:5173>

### 3. 生产预览（单端口）

```powershell
cd vue-app
npm run build

cd ..\fastapi-app
uvicorn main:app --host 127.0.0.1 --port 8000
```

打开 <http://127.0.0.1:8000> 即可同时访问前端与 API。

## 云端部署（推荐 Railway）

对于这个项目，推荐使用 **Railway**：它支持 Docker、GitHub 自动部署、托管 MySQL 和持久化 Volume，正好覆盖 FastAPI、Tortoise ORM 与图片上传的需求。GitHub Pages 只能托管静态页面，Vercel 的 Serverless 文件系统也不适合当前的上传与数据库连接方式。

仓库已经包含：

- `Dockerfile`：自动构建 Vue 前端，并由 FastAPI 单端口提供页面与 API
- `railway.json`：Dockerfile 构建、`/api/health` 健康检查和失败重启策略
- `.dockerignore`：排除本地数据库、虚拟环境与构建产物

### Railway 部署步骤

1. 在 Railway 中选择 **New Project → Deploy from GitHub repo**，连接 `wine1133/tunan-cake-shop`
2. 在同一个项目中添加 **MySQL** 服务
3. 为 Web 服务添加以下环境变量：

```env
DB_URL=${{MySQL.MYSQL_URL}}
SECRET_KEY=替换为一段足够长的随机字符串
DATA_DIR=/data/db
UPLOAD_DIR=/data/uploads
```

4. 给 Web 服务添加一个 Volume，并挂载到 `/data`
5. 在 **Settings → Networking** 中生成公开域名
6. 部署完成后访问 `https://你的域名/api/health`，确认返回 `code: "200"`

首次启动会自动建表并写入演示数据。上传图片与 SQLite 数据会保存在 `/data` Volume 中，重新部署不会丢失。

> 正式商用前请修改默认管理员密码、`SECRET_KEY`，并按需配置自定义域名与数据库备份。

## 体验账号

| 角色 | 账号 | 密码 | 入口 |
| --- | --- | --- | --- |
| 管理员 | `admin` | `admin123` | 登录页选择「管理后台」 |
| 顾客 | `user` | `user123` | 登录页选择「顾客登录」 |

其他演示顾客（仅用于后台数据展示）：`chenzhixia` / `suyue` / `zhouyu`，密码均为 `123456`。

## 切换到 MySQL 8

1. 导入 SQL：

```powershell
cmd /c "mysql -u root -p < sql\cake_shop.sql"
```

2. 在 `fastapi-app/.env` 中配置：

```env
DB_URL=mysql://root:你的密码@127.0.0.1:3306/cake_shop?charset=utf8mb4
SECRET_KEY=请替换成一段足够长的随机字符串
```

3. 重启后端。数据库已由 SQL 初始化时，不会重复写入种子数据。

> 如果不导入 SQL，也可以直接连接一个空 MySQL 数据库，Tortoise 会自动建表并执行种子初始化。

## API 文档

后端启动后访问：

- Swagger UI：<http://127.0.0.1:8000/docs>
- OpenAPI JSON：<http://127.0.0.1:8000/openapi.json>
- 健康检查：<http://127.0.0.1:8000/api/health>

统一响应示例：

```json
{
  "code": "200",
  "msg": "操作成功",
  "data": {}
}
```

## 配置项

`fastapi-app/.env`：

```env
DB_URL=sqlite://data/cake_shop.db
SECRET_KEY=replace-with-a-long-random-string
TOKEN_EXPIRE_HOURS=24
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## 上传说明

图片上传接口：`POST /api/files/upload`，支持 JPG / PNG / WebP / GIF，最大 5MB。文件保存在 `fastapi-app/static/uploads/`，通过 `/uploads/{filename}` 访问。

## 说明

- 本项目已实现完整的增删改查、权限校验、库存扣减与前端交互，不是静态页面。
- 默认账号仅用于本地演示，部署到公网前请务必修改密码与 `SECRET_KEY`。
- 产品图片来自 Unsplash，已下载到 `vue-app/public/images/`，不依赖外部图片服务即可展示。