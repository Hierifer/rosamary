from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from schemas.item import Item, ItemCreate, ItemUpdate
from services.item_service import ItemService

router = APIRouter()
item_service = ItemService()


@router.get("/", response_model=List[Item])
async def get_items(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词")
):
    """获取项目列表"""
    try:
        items = await item_service.get_items(skip=skip, limit=limit, search=search)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """根据ID获取项目"""
    item = await item_service.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="项目不存在")
    return item


@router.post("/", response_model=Item)
async def create_item(item_data: ItemCreate):
    """创建新项目"""
    try:
        item = await item_service.create_item(item_data)
        return item
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item_data: ItemUpdate):
    """更新项目信息"""
    item = await item_service.update_item(item_id, item_data)
    if not item:
        raise HTTPException(status_code=404, detail="项目不存在")
    return item


@router.delete("/{item_id}")
async def delete_item(item_id: int):
    """删除项目"""
    success = await item_service.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="项目不存在")
    return {"message": "项目删除成功"}
