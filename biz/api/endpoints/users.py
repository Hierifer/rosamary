from fastapi import APIRouter, HTTPException, Depends
from typing import List
from schemas.user import User, UserCreate, UserUpdate
from services.user_service import UserService

router = APIRouter()
user_service = UserService()


@router.get("/", response_model=List[User])
async def get_users(skip: int = 0, limit: int = 10):
    """获取用户列表"""
    try:
        users = await user_service.get_users(skip=skip, limit=limit)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """根据ID获取用户"""
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.post("/", response_model=User)
async def create_user(user_data: UserCreate):
    """创建新用户"""
    try:
        user = await user_service.create_user(user_data)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user_data: UserUpdate):
    """更新用户信息"""
    user = await user_service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """删除用户"""
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": "用户删除成功"}
