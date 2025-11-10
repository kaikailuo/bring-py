"""
资源相关的Pydantic数据验证模式
"""
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from app.models.resource import ResourceType, ResourceCategory
from app.schemas.user import ApiResponse  # 从user.py导入ApiResponse


class ResourceBase(BaseModel):
    """资源基础模式"""
    title: str
    description: Optional[str] = None
    type: ResourceType
    category: ResourceCategory
    course_id: Optional[str] = None
    course_name: Optional[str] = None

    @validator('title')
    def validate_title(cls, v):
        if len(v) < 1 or len(v) > 255:
            raise ValueError('资源标题长度应为1-255个字符')
        return v


class ResourceCreate(ResourceBase):
    """资源创建模式"""
    pass


class ResourceUpdate(BaseModel):
    """资源更新模式"""
    title: Optional[str] = None
    description: Optional[str] = None
    type: Optional[ResourceType] = None
    category: Optional[ResourceCategory] = None
    course_id: Optional[str] = None
    course_name: Optional[str] = None

    @validator('title')
    def validate_title(cls, v):
        if v is not None and (len(v) < 1 or len(v) > 255):
            raise ValueError('资源标题长度应为1-255个字符')
        return v


class ResourceResponse(ResourceBase):
    """资源响应模式"""
    id: int
    file_name: str
    format: str
    size: int
    downloads: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ResourceFileResponse(BaseModel):
    """资源文件响应模式"""
    file_name: str
    content_type: str
    file_path: str
    size: int


class ResourceListResponse(BaseModel):
    """资源列表响应模式"""
    total: int
    items: list[ResourceResponse]
    page: int
    page_size: int