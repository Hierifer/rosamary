from typing import List, Optional
from schemas.item import Item, ItemCreate, ItemUpdate
from datetime import datetime


class ItemService:
    """项目服务类"""
    
    def __init__(self):
        # 这里可以初始化数据库连接等
        self._items = []  # 模拟数据存储
        self._next_id = 1

    async def get_items(self, skip: int = 0, limit: int = 10, search: Optional[str] = None) -> List[Item]:
        """获取项目列表"""
        items = self._items
        
        # 如果有搜索关键词，进行过滤
        if search:
            items = [item for item in items if search.lower() in item.name.lower() or 
                    (item.description and search.lower() in item.description.lower())]
        
        return items[skip:skip + limit]

    async def get_item_by_id(self, item_id: int) -> Optional[Item]:
        """根据ID获取项目"""
        for item in self._items:
            if item.id == item_id:
                return item
        return None

    async def create_item(self, item_data: ItemCreate) -> Item:
        """创建新项目"""
        # 检查项目名称是否已存在
        for item in self._items:
            if item.name == item_data.name:
                raise ValueError("项目名称已存在")
        
        # 创建新项目
        new_item = Item(
            id=self._next_id,
            name=item_data.name,
            description=item_data.description,
            price=item_data.price,
            category=item_data.category,
            is_available=item_data.is_available,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self._items.append(new_item)
        self._next_id += 1
        return new_item

    async def update_item(self, item_id: int, item_data: ItemUpdate) -> Optional[Item]:
        """更新项目信息"""
        for i, item in enumerate(self._items):
            if item.id == item_id:
                # 更新项目信息
                update_data = item_data.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(item, field, value)
                item.updated_at = datetime.now()
                return item
        return None

    async def delete_item(self, item_id: int) -> bool:
        """删除项目"""
        for i, item in enumerate(self._items):
            if item.id == item_id:
                del self._items[i]
                return True
        return False
