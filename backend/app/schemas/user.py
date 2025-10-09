"""
用户相关的Pydantic数据验证模式
"""
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    """用户基础模式"""
    username: str
    name: str
    email: EmailStr
    role: UserRole

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
    """用户更新模式"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

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
    data: Optional[dict] = None

    @classmethod
    def success(cls, data=None, message="success"):
        """成功响应"""
        return cls(code=200, message=message, data=data)

    @classmethod
    def error(cls, code=400, message="error", data=None):
        """错误响应"""
        return cls(code=code, message=message, data=data)
