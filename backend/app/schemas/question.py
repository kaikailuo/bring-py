"""
问题相关的数据模式
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.schemas.user import ApiResponse


class QuestionCategoryCreate(BaseModel):
    """创建问题分类的请求模式"""
    name: str = Field(..., min_length=1, max_length=100, description="分类名称")
    description: Optional[str] = Field(None, description="分类描述")
    color: Optional[str] = Field("#409EFF", description="分类颜色")


class QuestionCategoryUpdate(BaseModel):
    """更新问题分类的请求模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="分类名称")
    description: Optional[str] = Field(None, description="分类描述")
    color: Optional[str] = Field(None, description="分类颜色")
    is_active: Optional[bool] = Field(None, description="是否激活")


class QuestionCategoryResponse(BaseModel):
    """问题分类响应模式"""
    id: int
    name: str
    description: Optional[str]
    color: str
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class QuestionCreate(BaseModel):
    """创建问题的请求模式"""
    title: str = Field(..., min_length=1, max_length=200, description="问题标题")
    content: str = Field(..., min_length=1, description="问题内容")
    category_id: Optional[int] = Field(None, description="问题分类ID")
    tags: Optional[str] = Field(None, description="问题标签，用逗号分隔")
    is_anonymous: bool = Field(False, description="是否匿名提问")


class QuestionUpdate(BaseModel):
    """更新问题的请求模式"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="问题标题")
    content: Optional[str] = Field(None, min_length=1, description="问题内容")
    category_id: Optional[int] = Field(None, description="问题分类ID")
    status: Optional[str] = Field(None, description="问题状态")
    priority: Optional[str] = Field(None, description="问题优先级")
    tags: Optional[str] = Field(None, description="问题标签，用逗号分隔")
    answer: Optional[str] = Field(None, description="问题答案")


class QuestionResponse(BaseModel):
    """问题响应模式"""
    id: int
    title: str
    content: str
    student_id: int
    teacher_id: Optional[int]
    category_id: Optional[int]
    status: Optional[str]
    priority: Optional[str]
    tags: List[str]
    answer: Optional[str]
    answer_time: Optional[datetime]
    is_anonymous: bool
    view_count: int
    like_count: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    student: Optional[Dict[str, Any]]
    teacher: Optional[Dict[str, Any]]
    category: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True


class QuestionReplyCreate(BaseModel):
    """创建问题回复的请求模式"""
    content: str = Field(..., min_length=1, description="回复内容")
    is_solution: bool = Field(False, description="是否为解决方案")


class QuestionReplyResponse(BaseModel):
    """问题回复响应模式"""
    id: int
    question_id: int
    user_id: int
    content: str
    is_teacher_reply: bool
    is_solution: bool
    like_count: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    user: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True


class QuestionSummaryCreate(BaseModel):
    """创建问题总结的请求模式"""
    title: str = Field(..., min_length=1, max_length=200, description="总结标题")
    summary_type: str = Field(..., description="总结类型（daily/weekly/monthly）")
    period_start: datetime = Field(..., description="统计开始时间")
    period_end: datetime = Field(..., description="统计结束时间")


class QuestionSummaryResponse(BaseModel):
    """问题总结响应模式"""
    id: int
    title: str
    content: str
    summary_type: str
    period_start: datetime
    period_end: datetime
    teacher_id: int
    question_count: int
    resolved_count: int
    pending_count: int
    category_stats: Dict[str, Any]
    common_issues: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    created_at: Optional[datetime]
    teacher: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True


class QuestionStatsResponse(BaseModel):
    """问题统计响应模式"""
    total_questions: int
    pending_questions: int
    answered_questions: int
    resolved_questions: int
    category_distribution: Dict[str, int]
    priority_distribution: Dict[str, int]
    daily_question_count: List[Dict[str, Any]]
    common_keywords: List[Dict[str, Any]]
    recent_questions: List[QuestionResponse]


class QuestionFilterParams(BaseModel):
    """问题筛选参数"""
    category_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    student_id: Optional[int] = None
    teacher_id: Optional[int] = None
    keyword: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    skip: int = 0
    limit: int = 20


class QuestionSummaryParams(BaseModel):
    """问题总结参数"""
    summary_type: str = Field(..., description="总结类型（daily/weekly/monthly）")
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")
    include_ai_analysis: bool = Field(True, description="是否包含AI分析")
