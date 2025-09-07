from fastapi import APIRouter
from .endpoints import health, users, items

router = APIRouter()

# 包含各个端点路由
router.include_router(health.router, prefix="/health", tags=["健康检查"])
router.include_router(users.router, prefix="/users", tags=["用户管理"])
router.include_router(items.router, prefix="/items", tags=["项目管理"])
