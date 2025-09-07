from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ItemBase(BaseModel):
    """项目基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="项目名称")
    description: Optional[str] = Field(None, max_length=500, description="项目描述")
    price: float = Field(..., ge=0, description="价格")
    category: str = Field(..., min_length=1, max_length=50, description="分类")
    is_available: bool = Field(True, description="是否可用")


class ItemCreate(ItemBase):
    """创建项目模型"""
    pass


class ItemUpdate(BaseModel):
    """更新项目模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="项目名称")
    description: Optional[str] = Field(None, max_length=500, description="项目描述")
    price: Optional[float] = Field(None, ge=0, description="价格")
    category: Optional[str] = Field(None, min_length=1, max_length=50, description="分类")
    is_available: Optional[bool] = Field(None, description="是否可用")


class Item(ItemBase):
    """项目响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
