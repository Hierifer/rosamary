from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from pathlib import Path


# 获取项目根目录
BASE_DIR = Path(__file__).parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    """应用配置设置"""
    
    # 基础配置
    PROJECT_NAME: str = "FastAPI Business Service"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    
    # 跨域配置
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # 数据库配置
    DATABASE_URL: Optional[str] = None
    
    # Redis 配置
    REDIS_URL: Optional[str] = None
    
    # JWT 配置
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    model_config = {
        "env_file": str(ENV_FILE),
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }




# 全局设置实例
try:
    settings = Settings()
    print(f"配置加载成功，端口: {settings.SERVER_PORT}")
except Exception as e:
    print(f"配置加载错误: {e}")
    # 使用默认配置
    settings = Settings()