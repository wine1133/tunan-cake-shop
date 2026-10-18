from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from tortoise import Tortoise

from common.exception_handler import (
    CustomException,
    custom_exception_handler,
    validation_exception_handler,
)
from common.result import Result
from routers import address, auth, category, dashboard, files, goods, notice, orders, user
from seed_data import seed_database
from settings import BASE_DIR, CORS_ORIGINS, DB_URL, UPLOAD_DIR

MODULES = {"models": ["models"]}
FRONTEND_DIST = BASE_DIR.parent / "vue-app" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(db_url=DB_URL, modules=MODULES)
    await Tortoise.generate_schemas()
    await seed_database()
    yield
    await Tortoise.close_connections()


app = FastAPI(
    title="兔南蛋糕零售店 API",
    description="蛋糕零售店：用户预订、订单管理、商品与内容管理接口",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(CustomException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

for router in (
    auth.router,
    user.router,
    category.router,
    goods.router,
    address.router,
    orders.router,
    notice.router,
    files.router,
    dashboard.router,
):
    app.include_router(router, prefix="/api")


@app.get("/api/health")
async def health():
    return Result.success({"status": "ok", "service": "tunan-cake-shop"})


@app.get("/", include_in_schema=False)
async def root():
    index = FRONTEND_DIST / "index.html"
    if index.exists():
        return FileResponse(index)
    return Result.success(
        {"name": "兔南蛋糕零售店", "docs": "/docs", "health": "/api/health"}
    )


@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback(full_path: str):
    """Serve the built Vue app so `uvicorn main:app` is a one-command preview."""
    index = FRONTEND_DIST / "index.html"
    if not index.exists():
        return Result.error("前端尚未构建，请先在 vue-app 目录运行 npm run build", "404")
    candidate = (FRONTEND_DIST / full_path).resolve()
    try:
        candidate.relative_to(FRONTEND_DIST.resolve())
    except ValueError:
        return FileResponse(index)
    if candidate.is_file():
        return FileResponse(candidate)
    return FileResponse(index)