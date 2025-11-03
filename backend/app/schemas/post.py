"""
帖子相关的Pydantic数据验证模式
"""
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime


class PostBase(BaseModel):
    """帖子基础模式"""
    title: str
    content: str
    category: str
    tags: Optional[List[str]] = []

    @validator('title')
    def validate_title(cls, v):
        if len(v) < 1 or len(v) > 200:
            raise ValueError('标题长度应为1-200个字符')
        return v

    @validator('content')
    def validate_content(cls, v):
        if len(v) < 1:
            raise ValueError('内容不能为空')
        return v

    @validator('category')
    def validate_category(cls, v):
        if not v:
            raise ValueError('分类不能为空')
        return v


class PostCreate(PostBase):
    """帖子创建模式"""
    pass


class PostUpdate(BaseModel):
    """帖子更新模式"""
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

    @validator('title')
    def validate_title(cls, v):
        if v is not None and (len(v) < 1 or len(v) > 200):
            raise ValueError('标题长度应为1-200个字符')
        return v

    @validator('content')
    def validate_content(cls, v):
        if v is not None and len(v) < 1:
            raise ValueError('内容不能为空')
        return v


class PostResponse(BaseModel):
    """帖子响应模式"""
    id: int
    title: str
    content: str
    category: str
    tags: List[str]
    author: dict
    views: int
    replies: int
    likes: int
    isFeatured: bool
    isPinned: bool
    time: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

