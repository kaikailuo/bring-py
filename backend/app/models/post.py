"""
帖子数据模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.utils.database import Base


class Post(Base):
    """帖子模型"""
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="帖子标题")
    content = Column(Text, nullable=False, comment="帖子内容")
    category = Column(String(50), nullable=False, index=True, comment="分类")
    tags = Column(JSON, default=list, comment="标签列表")
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="作者ID")
    views = Column(Integer, default=0, comment="浏览次数")
    replies = Column(Integer, default=0, comment="回复数")
    likes = Column(Integer, default=0, comment="点赞数")
    is_featured = Column(Boolean, default=False, comment="是否精华")
    is_pinned = Column(Boolean, default=False, comment="是否置顶")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关联关系
    author = relationship("User", backref="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', category='{self.category}')>"

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "tags": self.tags or [],
            "author": {
                "id": self.author.id if self.author else None,
                "name": self.author.name if self.author else "未知用户",
                "avatar": self.author.avatar if self.author and self.author.avatar else None,
                "role": self.author.role.value if self.author and self.author.role else None,
                "is_muted": self.author.is_muted if self.author else False
            },
            "time": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else "",
            "views": self.views,
            "replies": self.replies,
            "likes": self.likes,
            "isFeatured": self.is_featured,
            "isPinned": self.is_pinned,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
