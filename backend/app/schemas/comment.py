"""
评论相关的Pydantic数据验证模式
"""
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class CommentBase(BaseModel):
    """评论基础模式"""
    content: str
    parent_id: Optional[int] = None

    @validator('content')
    def validate_content(cls, v):
        if len(v) < 1:
            raise ValueError('评论内容不能为空')
        if len(v) > 1000:
            raise ValueError('评论内容不能超过1000个字符')
        return v


class CommentCreate(CommentBase):
    """评论创建模式"""
    # post_id 从URL路径获取，不需要在请求体中


class CommentUpdate(BaseModel):
    """评论更新模式"""
    content: str

    @validator('content')
    def validate_content(cls, v):
        if len(v) < 1:
            raise ValueError('评论内容不能为空')
        if len(v) > 1000:
            raise ValueError('评论内容不能超过1000个字符')
        return v


class CommentResponse(BaseModel):
    """评论响应模式"""
    id: int
    post_id: int
    content: str
    author: dict
    parent_id: Optional[int] = None
    likes: int
    time: str
    replies_count: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

