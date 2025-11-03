"""
问题相关的数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.utils.database import Base
import enum


class QuestionStatus(str, enum.Enum):
    """问题状态枚举"""
    PENDING = "pending"  # 待回答
    ANSWERED = "answered"  # 已回答
    RESOLVED = "resolved"  # 已解决
    CLOSED = "closed"  # 已关闭


class QuestionPriority(str, enum.Enum):
    """问题优先级枚举"""
    LOW = "low"  # 低优先级
    MEDIUM = "medium"  # 中优先级
    HIGH = "high"  # 高优先级
    URGENT = "urgent"  # 紧急


class QuestionCategory(Base):
    """问题分类模型"""
    __tablename__ = "question_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="分类名称")
    description = Column(Text, comment="分类描述")
    color = Column(String(20), default="#409EFF", comment="分类颜色")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关联关系
    questions = relationship("Question", back_populates="category")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "color": self.color,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Question(Base):
    """问题模型"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="问题标题")
    content = Column(Text, nullable=False, comment="问题内容")
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="提问学生ID")
    teacher_id = Column(Integer, ForeignKey("users.id"), comment="负责教师ID")
    category_id = Column(Integer, ForeignKey("question_categories.id"), comment="问题分类ID")
    status = Column(Enum(QuestionStatus), default=QuestionStatus.PENDING, comment="问题状态")
    priority = Column(Enum(QuestionPriority), default=QuestionPriority.MEDIUM, comment="问题优先级")
    tags = Column(String(500), comment="问题标签，用逗号分隔")
    answer = Column(Text, comment="问题答案")
    answer_time = Column(DateTime(timezone=True), comment="回答时间")
    is_anonymous = Column(Boolean, default=False, comment="是否匿名提问")
    view_count = Column(Integer, default=0, comment="查看次数")
    like_count = Column(Integer, default=0, comment="点赞次数")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关联关系
    student = relationship("User", foreign_keys=[student_id], backref="asked_questions")
    teacher = relationship("User", foreign_keys=[teacher_id], backref="answered_questions")
    category = relationship("QuestionCategory", back_populates="questions")
    replies = relationship("QuestionReply", back_populates="question", cascade="all, delete-orphan")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "student_id": self.student_id,
            "teacher_id": self.teacher_id,
            "category_id": self.category_id,
            "status": self.status.value if self.status else None,
            "priority": self.priority.value if self.priority else None,
            "tags": self.tags.split(",") if self.tags else [],
            "answer": self.answer,
            "answer_time": self.answer_time.isoformat() if self.answer_time else None,
            "is_anonymous": self.is_anonymous,
            "view_count": self.view_count,
            "like_count": self.like_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "student": self.student.to_dict() if self.student else None,
            "teacher": self.teacher.to_dict() if self.teacher else None,
            "category": self.category.to_dict() if self.category else None
        }


class QuestionReply(Base):
    """问题回复模型"""
    __tablename__ = "question_replies"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, comment="问题ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="回复用户ID")
    content = Column(Text, nullable=False, comment="回复内容")
    is_teacher_reply = Column(Boolean, default=False, comment="是否为教师回复")
    is_solution = Column(Boolean, default=False, comment="是否为解决方案")
    like_count = Column(Integer, default=0, comment="点赞次数")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")

    # 关联关系
    question = relationship("Question", back_populates="replies")
    user = relationship("User", backref="question_replies")

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "question_id": self.question_id,
            "user_id": self.user_id,
            "content": self.content,
            "is_teacher_reply": self.is_teacher_reply,
            "is_solution": self.is_solution,
            "like_count": self.like_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user": self.user.to_dict() if self.user else None
        }


class QuestionSummary(Base):
    """问题总结模型"""
    __tablename__ = "question_summaries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="总结标题")
    content = Column(Text, nullable=False, comment="总结内容")
    summary_type = Column(String(50), nullable=False, comment="总结类型（daily/weekly/monthly）")
    period_start = Column(DateTime(timezone=True), nullable=False, comment="统计开始时间")
    period_end = Column(DateTime(timezone=True), nullable=False, comment="统计结束时间")
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="生成总结的教师ID")
    question_count = Column(Integer, default=0, comment="问题总数")
    resolved_count = Column(Integer, default=0, comment="已解决问题数")
    pending_count = Column(Integer, default=0, comment="待解决问题数")
    category_stats = Column(Text, comment="分类统计（JSON格式）")
    common_issues = Column(Text, comment="常见问题（JSON格式）")
    recommendations = Column(Text, comment="改进建议（JSON格式）")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关联关系
    teacher = relationship("User", backref="question_summaries")

    def to_dict(self):
        """转换为字典"""
        import json
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "summary_type": self.summary_type,
            "period_start": self.period_start.isoformat() if self.period_start else None,
            "period_end": self.period_end.isoformat() if self.period_end else None,
            "teacher_id": self.teacher_id,
            "question_count": self.question_count,
            "resolved_count": self.resolved_count,
            "pending_count": self.pending_count,
            "category_stats": json.loads(self.category_stats) if self.category_stats else {},
            "common_issues": json.loads(self.common_issues) if self.common_issues else [],
            "recommendations": json.loads(self.recommendations) if self.recommendations else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "teacher": self.teacher.to_dict() if self.teacher else None
        }
