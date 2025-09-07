from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "message": "服务运行正常"
    }


@router.get("/detailed")
async def detailed_health_check():
    """详细健康检查"""
    return {
        "status": "healthy",
        "timestamp": "2025-09-02T00:00:00Z",
        "version": "1.0.0",
        "environment": "development",
        "services": {
            "database": "connected",
            "cache": "connected"
        }
    }
