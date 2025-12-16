"""
收藏数据模型
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.utils.database import Base


class Favorite(Base):
    """收藏模型"""
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, comment="帖子ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="收藏时间")

    # 唯一约束：一个用户只能收藏一个帖子一次
    __table_args__ = (
        UniqueConstraint('post_id', 'user_id', name='uq_post_user'),
    )

    # 关联关系
    post = relationship("Post", back_populates="favorites")
    user = relationship("User", backref="favorites")

    def __repr__(self):
        return f"<Favorite(id={self.id}, post_id={self.post_id}, user_id={self.user_id})>"

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


