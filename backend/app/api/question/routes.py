"""
问题相关的API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta

from app.utils.database import get_db
from app.services.question import QuestionService
from app.schemas.question import (
    QuestionCreate, QuestionUpdate, QuestionResponse, QuestionCategoryCreate, 
    QuestionCategoryUpdate, QuestionCategoryResponse, QuestionReplyCreate, 
    QuestionReplyResponse, QuestionSummaryCreate, QuestionSummaryResponse,
    QuestionStatsResponse, QuestionFilterParams, QuestionSummaryParams
)
from app.schemas.user import ApiResponse
from app.utils.security import get_current_active_user
from app.models.user import User

# 创建路由器
router = APIRouter(prefix="/questions", tags=["问题管理"])


# 问题分类相关接口
@router.post("/categories", response_model=ApiResponse, summary="创建问题分类")
async def create_question_category(
    category_data: QuestionCategoryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建问题分类（仅教师和管理员可用）"""
    if current_user.role not in ["teacher", "admin"]:
        return ApiResponse.error(code=403, message="权限不足")
    
    try:
        question_service = QuestionService(db)
        category = question_service.create_category(category_data)
        
        return ApiResponse.success(
            data={"category": QuestionCategoryResponse.from_orm(category).dict()},
            message="创建分类成功"
        )
    except Exception as e:
        return ApiResponse.error(code=500, message=f"创建分类失败: {str(e)}")


@router.get("/categories", response_model=ApiResponse, summary="获取问题分类列表")
async def get_question_categories(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="限制返回的记录数"),
    db: Session = Depends(get_db)
):
    """获取问题分类列表"""
    try:
        question_service = QuestionService(db)
        categories = question_service.get_categories(skip, limit)
        
        category_list = [QuestionCategoryResponse.from_orm(cat).dict() for cat in categories]
        
        return ApiResponse.success(
            data={"categories": category_list},
            message="获取分类列表成功"
        )
    except Exception as e:
        return ApiResponse.error(code=500, message=f"获取分类列表失败: {str(e)}")


@router.put("/categories/{category_id}", response_model=ApiResponse, summary="更新问题分类")
async def update_question_category(
    category_id: int,
    category_data: QuestionCategoryUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新问题分类（仅教师和管理员可用）"""
    if current_user.role not in ["teacher", "admin"]:
        return ApiResponse.error(code=403, message="权限不足")
    
    try:
        question_service = QuestionService(db)
        category = question_service.update_category(category_id, category_data)
        
        if not category:
            return ApiResponse.error(code=404, message="分类不存在")
        
        return ApiResponse.success(
            data={"category": QuestionCategoryResponse.from_orm(category).dict()},
            message="更新分类成功"
        )
    except Exception as e:
        return ApiResponse.error(code=500, message=f"更新分类失败: {str(e)}")


@router.delete("/categories/{category_id}", response_model=ApiResponse, summary="删除问题分类")
async def delete_question_category(
    category_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除问题分类（仅管理员可用）"""
    if current_user.role != "admin":
        return ApiResponse.error(code=403, message="权限不足")
    
    try:
        question_service = QuestionService(db)
        success = question_service.delete_category(category_id)
        
        if not success:
            return ApiResponse.error(code=404, message="分类不存在")
        
        return ApiResponse.success(message="删除分类成功")
    except Exception as e:
        return ApiResponse.error(code=500, message=f"删除分类失败: {str(e)}")


# 问题相关接口
@router.post("", response_model=ApiResponse, summary="创建问题")
async def create_question(
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建问题（学生可用）"""
    if current_user.role not in ["student", "teacher", "admin"]:
        return ApiResponse.error(code=403, message="权限不足")
    
    try:
        question_service = QuestionService(db)
        question = question_service.create_question(question_data, current_user.id)
        
        return ApiResponse.success(
            data={"question": QuestionResponse.from_orm(question).dict()},
            message="创建问题成功"
        )
    except Exception as e:
        return ApiResponse.error(code=500, message=f"创建问题失败: {str(e)}")


@router.get("", response_model=ApiResponse, summary="获取问题列表")
async def get_questions(
    category_id: Optional[int] = Query(None, description="分类ID"),
    status: Optional[str] = Query(None, description="问题状态"),
    priority: Optional[str] = Query(None, description="问题优先级"),
    student_id: Optional[int] = Query(None, description="学生ID"),
    teacher_id: Optional[int] = Query(None, description="教师ID"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    start_date: Optional[datetime] = Query(None, description="开始日期"),
    end_date: Optional[datetime] = Query(None, description="结束日期"),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="限制返回的记录数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取问题列表"""
    try:
        # 权限控制：学生只能看到自己的问题，教师和管理员可以看到所有问题
        filters = QuestionFilterParams(
            category_id=category_id,
            status=status,
            priority=priority,
            student_id=student_id if current_user.role == "student" else student_id,
            teacher_id=teacher_id,
            keyword=keyword,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit
        )
        
        # 如果是学生，只能查看自己的问题
        if current_user.role == "student":
            filters.student_id = current_user.id
        
        question_service = QuestionService(db)
        questions = question_service.get_questions(filters)
        
        question_list = [QuestionResponse.from_orm(q).dict() for q in questions]
        
        return ApiResponse.success(
            data={"questions": question_list},
            message="获取问题列表成功"
        )
    except Exception as e:
        return ApiResponse.error(code=500, message=f"获取问题列表失败: {str(e)}")


@router.get("/{question_id}", response_model=ApiResponse, summary="获取问题详情")
async def get_question(
    question_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取问题详情"""
    try:
        question_service = QuestionService(db)
        question = question_service.get_question_by_id(question_id)
        
        if not question:
            return ApiResponse.error(code=404, message="问题不存在")
        
        # 权限控制：学生只能查看自己的问题
        if current_user.role == "student" and question.student_id != current_user.id:
            return ApiResponse.error(code=403, message="权限不足")
        
        # 增加查看次数
        question.view_count += 1
        db.commit()
        
        return ApiResponse.success(
            data={"question": QuestionResponse.from_orm(question).dict()},
            message="获取问题详情成功"
        )
    except Exception as e:
        return ApiResponse.error(code=500, message=f"获取问题详情失败: {str(e)}")


@router.put("/{question_id}", response_model=ApiResponse, summary="更新问题")
async def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新问题"""
    try:
        question_service = QuestionService(db)
        question = question_service.get_question_by_id(question_id)
        
        if not question:
            return ApiResponse.error(code=404, message="问题不存在")
        
        # 权限控制：学生只能更新自己的问题，教师可以更新分配给自己的问题
        if current_user.role == "student" and question.student_id != current_user.id:
            return ApiResponse.error(code=403, message="权限不足")
        elif current_user.role == "teacher" and question.teacher_id != current_user.id:
            return ApiResponse.error(code=403, message="权限不足")
        
        updated_question = question_service.update_question(question_id, question_data)
        
        return ApiResponse.success(
            data={"question": QuestionResponse.from_orm(updated_question).dict()},
            message="更新问题成功"
        )
    except Exception as e:
        return ApiResponse.error(code=500, message=f"更新问题失败: {str(e)}")


@router.post("/{question_id}/assign", response_model=ApiResponse, summary="分配问题给教师")
async def assign_question(
    question_id: int,
    teacher_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """分配问题给教师（仅教师和管理员可用）"""
    if current_user.role not in ["teacher", "admin"]:
        return ApiResponse.error(code=403, message="权限不足")
    
    try:
        question_service = QuestionService(db)
        question = question_service.assign_question(question_id, teacher_id)
        
        if not question:
            return ApiResponse.error(code=404, message="问题不存在")
        
        return ApiResponse.success(
            data={"question": QuestionResponse.from_orm(question).dict()},
            message="分配问题成功"
        )
    except Exception as e:
        return ApiResponse.error(code=500, message=f"分配问题失败: {str(e)}")


# 问题回复相关接口
@router.post("/{question_id}/replies", response_model=ApiResponse, summary="创建问题回复")
async def create_question_reply(
    question_id: int,
    reply_data: QuestionReplyCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建问题回复"""
    try:
        question_service = QuestionService(db)
        reply = question_service.create_reply(question_id, reply_data, current_user.id)
        
        if not reply:
            return ApiResponse.error(code=404, message="问题不存在")
        
        return ApiResponse.success(
            data={"reply": QuestionReplyResponse.from_orm(reply).dict()},
            message="创建回复成功"
        )
    except Exception as e:
        return ApiResponse.error(code=500, message=f"创建回复失败: {str(e)}")


@router.get("/{question_id}/replies", response_model=ApiResponse, summary="获取问题回复列表")
async def get_question_replies(
    question_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取问题回复列表"""
    try:
        question_service = QuestionService(db)
        replies = question_service.get_question_replies(question_id)
        
        reply_list = [QuestionReplyResponse.from_orm(reply).dict() for reply in replies]
        
        return ApiResponse.success(
            data={"replies": reply_list},
            message="获取回复列表成功"
        )
    except Exception as e:
        return ApiResponse.error(code=500, message=f"获取回复列表失败: {str(e)}")


# 问题统计相关接口
@router.get("/stats/overview", response_model=ApiResponse, summary="获取问题统计概览")
async def get_question_stats(
    days: int = Query(30, ge=1, le=365, description="统计天数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取问题统计概览（仅教师和管理员可用）"""
    if current_user.role not in ["teacher", "admin"]:
        return ApiResponse.error(code=403, message="权限不足")
    
    try:
        question_service = QuestionService(db)
        teacher_id = current_user.id if current_user.role == "teacher" else None
        stats = question_service.get_question_stats(teacher_id, days)
        
        return ApiResponse.success(
            data={"stats": stats},
            message="获取统计信息成功"
        )
    except Exception as e:
        return ApiResponse.error(code=500, message=f"获取统计信息失败: {str(e)}")


# 问题总结相关接口
@router.post("/summaries", response_model=ApiResponse, summary="生成问题总结")
async def generate_question_summary(
    params: QuestionSummaryParams,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """生成问题总结（仅教师和管理员可用）"""
    if current_user.role not in ["teacher", "admin"]:
        return ApiResponse.error(code=403, message="权限不足")
    
    try:
        question_service = QuestionService(db)
        summary = question_service.generate_question_summary(params, current_user.id)
        
        return ApiResponse.success(
            data={"summary": QuestionSummaryResponse.from_orm(summary).dict()},
            message="生成问题总结成功"
        )
    except Exception as e:
        return ApiResponse.error(code=500, message=f"生成问题总结失败: {str(e)}")


@router.get("/summaries", response_model=ApiResponse, summary="获取问题总结列表")
async def get_question_summaries(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="限制返回的记录数"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取问题总结列表（仅教师和管理员可用）"""
    if current_user.role not in ["teacher", "admin"]:
        return ApiResponse.error(code=403, message="权限不足")
    
    try:
        question_service = QuestionService(db)
        teacher_id = current_user.id if current_user.role == "teacher" else None
        summaries = question_service.get_summaries(teacher_id, skip, limit)
        
        summary_list = [QuestionSummaryResponse.from_orm(summary).dict() for summary in summaries]
        
        return ApiResponse.success(
            data={"summaries": summary_list},
            message="获取总结列表成功"
        )
    except Exception as e:
        return ApiResponse.error(code=500, message=f"获取总结列表失败: {str(e)}")


@router.get("/summaries/{summary_id}", response_model=ApiResponse, summary="获取问题总结详情")
async def get_question_summary(
    summary_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取问题总结详情（仅教师和管理员可用）"""
    if current_user.role not in ["teacher", "admin"]:
        return ApiResponse.error(code=403, message="权限不足")
    
    try:
        question_service = QuestionService(db)
        summary = question_service.get_summary_by_id(summary_id)
        
        if not summary:
            return ApiResponse.error(code=404, message="总结不存在")
        
        # 权限控制：教师只能查看自己的总结
        if current_user.role == "teacher" and summary.teacher_id != current_user.id:
            return ApiResponse.error(code=403, message="权限不足")
        
        return ApiResponse.success(
            data={"summary": QuestionSummaryResponse.from_orm(summary).dict()},
            message="获取总结详情成功"
        )
    except Exception as e:
        return ApiResponse.error(code=500, message=f"获取总结详情失败: {str(e)}")
