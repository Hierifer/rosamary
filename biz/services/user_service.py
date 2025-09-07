from typing import List, Optional
from schemas.user import User, UserCreate, UserUpdate
from datetime import datetime


class UserService:
    """用户服务类"""
    
    def __init__(self):
        # 这里可以初始化数据库连接等
        self._users = []  # 模拟数据存储
        self._next_id = 1

    async def get_users(self, skip: int = 0, limit: int = 10) -> List[User]:
        """获取用户列表"""
        return self._users[skip:skip + limit]

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        for user in self._users:
            if user.id == user_id:
                return user
        return None

    async def create_user(self, user_data: UserCreate) -> User:
        """创建新用户"""
        # 检查用户名是否已存在
        for user in self._users:
            if user.username == user_data.username:
                raise ValueError("用户名已存在")
        
        # 创建新用户
        new_user = User(
            id=self._next_id,
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            is_active=user_data.is_active,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self._users.append(new_user)
        self._next_id += 1
        return new_user

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """更新用户信息"""
        for i, user in enumerate(self._users):
            if user.id == user_id:
                # 更新用户信息
                update_data = user_data.model_dump(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(user, field, value)
                user.updated_at = datetime.now()
                return user
        return None

    async def delete_user(self, user_id: int) -> bool:
        """删除用户"""
        for i, user in enumerate(self._users):
            if user.id == user_id:
                del self._users[i]
                return True
        return False
