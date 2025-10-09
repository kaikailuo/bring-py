"""
认证相关的API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.services.auth import AuthService
from app.schemas.user import (
    UserCreate, 
    UserLogin, 
    UserResponse, 
    ApiResponse,
    LoginResponse
)
from app.utils.security import get_current_active_user
from app.models.user import User

# 创建路由器
router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=ApiResponse, summary="用户注册")
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    用户注册接口
    
    - **username**: 用户名（3-20字符）
    - **password**: 密码（6-20字符）
    - **role**: 用户角色（student/teacher）
    - **name**: 真实姓名（2-10字符）
    - **email**: 邮箱地址
    """
    try:
        auth_service = AuthService(db)
        user = auth_service.create_user(user_data)
        
        return ApiResponse.success(
            data={
                "user": UserResponse.from_orm(user).dict()
            },
            message="注册成功"
        )
    except HTTPException as e:
        return ApiResponse.error(
            code=e.status_code,
            message=e.detail
        )
    except Exception as e:
        return ApiResponse.error(
            code=500,
            message=f"注册失败: {str(e)}"
        )


@router.post("/login", response_model=ApiResponse, summary="用户登录")
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    用户登录接口
    
    - **username**: 用户名
    - **password**: 密码
    """
    try:
        auth_service = AuthService(db)
        login_result = auth_service.login_user(login_data)
        
        return ApiResponse.success(
            data={
                "token": login_result.token,
                "user": login_result.user.dict()
            },
            message="登录成功"
        )
    except HTTPException as e:
        return ApiResponse.error(
            code=e.status_code,
            message=e.detail
        )
    except Exception as e:
        return ApiResponse.error(
            code=500,
            message=f"登录失败: {str(e)}"
        )


@router.post("/logout", response_model=ApiResponse, summary="用户登出")
async def logout(
    current_user: User = Depends(get_current_active_user)
):
    """
    用户登出接口
    
    注意：由于使用JWT令牌，客户端需要主动删除令牌
    """
    return ApiResponse.success(
        data={
            "user_id": current_user.id,
            "username": current_user.username
        },
        message="登出成功"
    )


@router.get("/me", response_model=ApiResponse, summary="获取当前用户信息")
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    获取当前用户信息接口
    """
    return ApiResponse.success(
        data={
            "user": UserResponse.from_orm(current_user).dict()
        },
        message="获取用户信息成功"
    )


@router.put("/me", response_model=ApiResponse, summary="更新当前用户信息")
async def update_current_user_info(
    user_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新当前用户信息接口
    
    - **name**: 真实姓名（可选）
    - **email**: 邮箱地址（可选）
    """
    try:
        auth_service = AuthService(db)
        updated_user = auth_service.update_user(current_user.id, user_data)
        
        return ApiResponse.success(
            data={
                "user": UserResponse.from_orm(updated_user).dict()
            },
            message="更新用户信息成功"
        )
    except HTTPException as e:
        return ApiResponse.error(
            code=e.status_code,
            message=e.detail
        )
    except Exception as e:
        return ApiResponse.error(
            code=500,
            message=f"更新用户信息失败: {str(e)}"
        )


@router.post("/change-password", response_model=ApiResponse, summary="修改密码")
async def change_password(
    old_password: str,
    new_password: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    修改密码接口
    
    - **old_password**: 原密码
    - **new_password**: 新密码（6-20字符）
    """
    try:
        auth_service = AuthService(db)
        auth_service.change_password(current_user.id, old_password, new_password)
        
        return ApiResponse.success(
            message="密码修改成功"
        )
    except HTTPException as e:
        return ApiResponse.error(
            code=e.status_code,
            message=e.detail
        )
    except Exception as e:
        return ApiResponse.error(
            code=500,
            message=f"密码修改失败: {str(e)}"
        )


# 管理员专用接口
@router.get("/users", response_model=ApiResponse, summary="获取用户列表（管理员）")
async def get_users(
    skip: int = 0,
    limit: int = 100,
    role: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    获取用户列表接口（仅管理员可用）
    
    - **skip**: 跳过的记录数
    - **limit**: 限制返回的记录数
    - **role**: 按角色筛选（可选）
    """
    if current_user.role != "admin":
        return ApiResponse.error(
            code=403,
            message="权限不足"
        )
    
    try:
        auth_service = AuthService(db)
        
        if role:
            users = auth_service.get_users_by_role(role, skip, limit)
        else:
            users = auth_service.get_all_users(skip, limit)
        
        user_list = [UserResponse.from_orm(user).dict() for user in users]
        
        return ApiResponse.success(
            data={
                "users": user_list,
                "total": len(user_list)
            },
            message="获取用户列表成功"
        )
    except Exception as e:
        return ApiResponse.error(
            code=500,
            message=f"获取用户列表失败: {str(e)}"
        )


@router.put("/users/{user_id}/activate", response_model=ApiResponse, summary="激活用户（管理员）")
async def activate_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    激活用户接口（仅管理员可用）
    """
    if current_user.role != "admin":
        return ApiResponse.error(
            code=403,
            message="权限不足"
        )
    
    try:
        auth_service = AuthService(db)
        auth_service.activate_user(user_id)
        
        return ApiResponse.success(
            message="用户激活成功"
        )
    except HTTPException as e:
        return ApiResponse.error(
            code=e.status_code,
            message=e.detail
        )
    except Exception as e:
        return ApiResponse.error(
            code=500,
            message=f"用户激活失败: {str(e)}"
        )


@router.put("/users/{user_id}/deactivate", response_model=ApiResponse, summary="停用用户（管理员）")
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    停用用户接口（仅管理员可用）
    """
    if current_user.role != "admin":
        return ApiResponse.error(
            code=403,
            message="权限不足"
        )
    
    try:
        auth_service = AuthService(db)
        auth_service.deactivate_user(user_id)
        
        return ApiResponse.success(
            message="用户停用成功"
        )
    except HTTPException as e:
        return ApiResponse.error(
            code=e.status_code,
            message=e.detail
        )
    except Exception as e:
        return ApiResponse.error(
            code=500,
            message=f"用户停用失败: {str(e)}"
        )
