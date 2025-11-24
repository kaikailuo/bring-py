"""
用户数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from app.utils.database import Base
import enum




class UserRole(str, enum.Enum):
    """用户角色枚举"""
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    role = Column(Enum(UserRole), nullable=False, default=UserRole.STUDENT, comment="用户角色")
    name = Column(String(100), nullable=False, comment="真实姓名")
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱地址")

    # -------------------------
    # 🆕 个人资料新增字段
    # -------------------------
    avatar = Column(String(255), nullable=True, comment="头像 URL")
    nickname = Column(String(100), nullable=True, comment="昵称")
    bio = Column(String(500), nullable=True, comment="个人简介")
    gender = Column(String(20), nullable=True, comment="性别（male/female/other）")
    phone = Column(String(50), nullable=True, comment="手机号")
    # -------------------------

    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role.value,
            "name": self.name,
            "email": self.email,

            # 🆕 新增个人资料字段
            "avatar": self.avatar,
            "nickname": self.nickname,
            "bio": self.bio,
            "gender": self.gender,
            "phone": self.phone,

            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
