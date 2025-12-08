"""
学生答题结果模型
记录每个学生在某个题目的提交次数、是否通过、最后提交时间等简要信息
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.utils.database import Base


class StudentResult(Base):
    __tablename__ = 'student_results'

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='学生ID')
    lesson = Column(String(100), nullable=True, comment='课次/目录')
    problem = Column(String(100), nullable=True, comment='题目标识')
    attempts = Column(Integer, default=0, comment='提交次数')
    passed = Column(Boolean, default=False, comment='是否通过')
    last_submitted_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment='最后提交时间')

    student = relationship('User', backref='test_results')

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'lesson': self.lesson,
            'problem': self.problem,
            'attempts': self.attempts,
            'passed': bool(self.passed),
            'last_submitted_at': self.last_submitted_at.isoformat() if self.last_submitted_at else None
        }
