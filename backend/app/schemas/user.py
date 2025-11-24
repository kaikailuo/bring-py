"""
用户相关的Pydantic数据验证模式
"""
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, Union
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    """用户基础模式"""
    username: str
    name: str
    email: EmailStr
    role: UserRole

    # -------------------------
    # 🆕 新增：基础展示所需的个人资料字段
    # （这些字段不会用于创建，只用于读取/响应）
    # -------------------------
    avatar: Optional[str] = None
    nickname: Optional[str] = None
    bio: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    # -------------------------

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3 or len(v) > 20:
            raise ValueError('用户名长度应为3-20个字符')
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('用户名只能包含字母、数字、下划线和连字符')
        return v

    @validator('name')
    def validate_name(cls, v):
        if len(v) < 2 or len(v) > 10:
            raise ValueError('姓名长度应为2-10个字符')
        return v


class UserCreate(UserBase):
    """用户创建模式"""
    password: str

    # 创建用户时不能传 nickname/avatar/bio 等
    class Config:
        extra = "ignore"

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6 or len(v) > 20:
            raise ValueError('密码长度应为6-20个字符')
        return v


class UserLogin(BaseModel):
    """用户登录模式"""
    username: str
    password: str

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3 or len(v) > 20:
            raise ValueError('用户名长度应为3-20个字符')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6 or len(v) > 20:
            raise ValueError('密码长度应为6-20个字符')
        return v


class UserUpdate(BaseModel):
    """用户更新模式（管理员或自身更新基础信息）"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

    # 🔥 注意：这是系统级更新，不包含 profile 字段
    # profile 字段单独走 UserProfileUpdate（更安全）

    @validator('name')
    def validate_name(cls, v):
        if v is not None and (len(v) < 2 or len(v) > 10):
            raise ValueError('姓名长度应为2-10个字符')
        return v

    @validator('password')
    def validate_password(cls, v):
        if v is not None and (len(v) < 6 or len(v) > 20):
            raise ValueError('密码长度应为6-20个字符')
        return v


# -------------------------
# 🆕 新增：用户个人资料更新模式
# -------------------------
class UserProfileUpdate(BaseModel):
    """用户个人资料更新（前端用户可自由修改）"""
    avatar: Optional[str] = None
    nickname: Optional[str] = None
    bio: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        extra = "ignore"

    @validator('nickname')
    def validate_nickname(cls, v):
        if v is not None and len(v) > 20:
            raise ValueError('昵称长度不能超过20字符')
        return v

    @validator('bio')
    def validate_bio(cls, v):
        if v is not None and len(v) > 300:
            raise ValueError('简介最多300字')
        return v
# -------------------------


class UserInDB(UserBase):
    """数据库中的用户模式"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """用户响应模式（不包含敏感信息）"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """令牌模式"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """令牌数据模式"""
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[UserRole] = None


class LoginResponse(BaseModel):
    """登录响应模式"""
    token: str
    user: UserResponse


class ApiResponse(BaseModel):
    """统一API响应模式"""
    code: int
    message: str
    data: Optional[Union[dict, list]] = None

    @classmethod
    def success(cls, data=None, message="success"):
        """成功响应"""
        return cls(code=200, message=message, data=data)

    @classmethod
    def error(cls, code=400, message="error", data=None):
        """错误响应"""
        return cls(code=code, message=message, data=data)

