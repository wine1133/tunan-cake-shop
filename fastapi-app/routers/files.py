import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile

from common.exception_handler import CustomException
from common.result import Result
from common.security import get_current_account
from settings import UPLOAD_DIR

router = APIRouter(prefix="/files", tags=["文件上传"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_SIZE = 5 * 1024 * 1024


@router.post("/upload")
async def upload(file: UploadFile = File(...), _: dict = Depends(get_current_account)):
    if file.content_type not in ALLOWED_TYPES:
        raise CustomException("仅支持 JPG、PNG、WebP 或 GIF 图片")
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise CustomException("图片不能超过 5MB")
    suffix = Path(file.filename or "image.jpg").suffix.lower() or ".jpg"
    if suffix not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        suffix = ".jpg"
    filename = f"{uuid.uuid4().hex}{suffix}"
    (UPLOAD_DIR / filename).write_bytes(content)
    return Result.success(f"/uploads/{filename}", "图片上传成功")