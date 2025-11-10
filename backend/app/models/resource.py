"""
资源数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.utils.database import Base
import enum


class ResourceType(str, enum.Enum):
    """资源类型枚举"""
    PPT = "ppt"
    PDF = "pdf"
    DOC = "doc"
    VIDEO = "video"
    OTHER = "other"


class ResourceCategory(str, enum.Enum):
    """资源分类枚举"""
    COURSEWARE = "courseware"
    REFERENCE = "reference"
    ASSIGNMENT = "assignment"
    OTHER = "other"


class Resource(Base):
    """资源模型"""
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, comment="资源标题")
    description = Column(Text, nullable=True, comment="资源描述")
    file_path = Column(String(255), nullable=False, comment="文件路径")
    file_name = Column(String(255), nullable=False, comment="文件名")
    format = Column(String(50), nullable=False, comment="文件格式")
    size = Column(Integer, nullable=False, comment="文件大小(字节)")
    type = Column(Enum(ResourceType), nullable=False, default=ResourceType.OTHER, comment="资源类型")
    category = Column(Enum(ResourceCategory), nullable=False, default=ResourceCategory.OTHER, comment="资源分类")
    downloads = Column(Integer, default=0, comment="下载次数")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False, comment="创建者ID")
    course_id = Column(String(50), nullable=True, comment="关联课程ID")
    course_name = Column(String(100), nullable=True, comment="关联课程名称")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # 关系定义
    creator = relationship("User", back_populates="resources")

    def __repr__(self):
        return f"<Resource(id={self.id}, title='{self.title}', type='{self.type}')>"

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "file_name": self.file_name,
            "format": self.format,
            "size": self.size,
            "type": self.type.value,
            "category": self.category.value,
            "downloads": self.downloads,
            "created_by": self.created_by,
            "course_id": self.course_id,
            "course_name": self.course_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# 在User模型中添加关系
from app.models.user import User
User.resources = relationship("Resource", back_populates="creator", cascade="all, delete-orphan")