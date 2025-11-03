"""
评论数据模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.utils.database import Base


class Comment(Base):
    """评论模型"""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False, comment="帖子ID")
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="评论者ID")
    content = Column(Text, nullable=False, comment="评论内容")
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True, comment="父评论ID（用于回复）")
    likes = Column(Integer, default=0, comment="点赞数")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    is_deleted = Column(Boolean, default=False, comment="是否已删除")

    # 关联关系
    post = relationship("Post", backref="comments")
    author = relationship("User", backref="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")

    def __repr__(self):
        return f"<Comment(id={self.id}, post_id={self.post_id}, author_id={self.author_id})>"

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "post_id": self.post_id,
            "content": self.content,
            "author": {
                "id": self.author.id if self.author else None,
                "name": self.author.name if self.author else "未知用户",
                "avatar": ""
            },
            "parent_id": self.parent_id,
            "likes": self.likes,
            "time": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else "",
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "replies_count": len([r for r in self.replies if not r.is_deleted]) if self.replies else 0
        }


