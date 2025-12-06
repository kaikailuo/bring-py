from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.models.student_result import StudentResult
from app.models.user import User, UserRole
from app.utils.security import get_current_user
from app.schemas.user import ApiResponse

router = APIRouter(prefix='/ai', tags=['AI'])


class AISummarizeRequest(BaseModel):
    post_id: int


class AISummarizeResponse(BaseModel):
    post_id: int
    status: str
    summary: Optional[str] = None


@router.post('/summarize', response_model=AISummarizeResponse)
async def summarize_post(req: AISummarizeRequest):
    """
    调用 summarize 逻辑：同步等待 summarize_post 返回字符串摘要
    返回结构：{ post_id, status: 'ok', summary }
    """
    try:
        from app.services.ai.tasks.summarize import summarize_post as summarize_impl
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'未找到 summarize 实现: {e}')

    try:
        summary = await summarize_impl(req.post_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        'post_id': req.post_id,
        'status': 'ok',
        'summary': summary
    }


class AIChatRequest(BaseModel):
    message: str
    post_id: Optional[int] = None


class AIChatResponse(BaseModel):
    reply: str


@router.post('/chat', response_model=AIChatResponse)
async def chat_endpoint(req: AIChatRequest):
    """
    占位：聊天接口。优先调用后端已有的 ai 任务处理器（如果实现了），否则返回占位回复。
    后端实现建议：在 `app.services.ai.tasks.chat` 中实现一个 `handle_chat(message, post_id=None)` 函数并返回字符串回复或异步结果。
    """
    # 尝试导入后端实现（如果存在）
    handler = None
    try:
        from app.services.ai.tasks.chat import handle_chat
        handler = handle_chat
    except Exception:
        handler = None

    if handler:
        try:
            result = handler(req.message, post_id=req.post_id)
            # 如果返回 coroutine，则 await
            if hasattr(result, '__await__'):
                result = await result
            return { 'reply': result or '（占位）未生成回复' }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Fallback 占位回复
    short = (req.message or '')[:200]
    return { 'reply': f'（占位回复）已收到消息：{short}' }


class AIAnalyzeStudentRequest(BaseModel):
    student_id: int


class AIAnalyzeStudentResponse(BaseModel):
    student_id: int
    status: str
    analysis: Optional[str] = None


@router.post('/analyze-student', response_model=ApiResponse, summary="AI分析学生答题情况")
async def analyze_student(
    req: AIAnalyzeStudentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print("调用后端API")
    
    """
    AI分析学生答题情况（仅教师和管理员可访问）
    接收学生ID，分析该学生的答题情况并返回分析结果
    """
    try:
        # 检查权限
        if current_user.role not in (UserRole.TEACHER, UserRole.ADMIN):
            raise HTTPException(status_code=403, detail="无权访问此资源")
        
        # 获取学生信息
        student = db.query(User).filter(
            User.id == req.student_id,
            User.role == UserRole.STUDENT
        ).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="学生不存在")
        
        # 获取该学生的所有答题记录
        results = db.query(StudentResult).filter(
            StudentResult.student_id == req.student_id
        ).all()
        
        if not results:
            return ApiResponse.success(
                data={
                    "student_id": req.student_id,
                    "status": "ok",
                    "analysis": f"{student.name} 同学目前还没有答题记录，建议鼓励其开始练习。"
                },
                message="分析完成"
            )
        
        # 统计信息
        total_attempts = sum(r.attempts for r in results)
        total_passed = sum(1 for r in results if r.passed)
        total_problems = len(set((r.lesson, r.problem) for r in results if r.lesson and r.problem))
        pass_rate = round((total_passed / total_problems * 100) if total_problems > 0 else 0, 2)
        
        # 按课程分组统计
        lesson_stats = {}
        for result in results:
            lesson_key = result.lesson or "未分类"
            if lesson_key not in lesson_stats:
                lesson_stats[lesson_key] = {
                    "total": 0,
                    "passed": 0,
                    "attempts": 0
                }
            lesson_stats[lesson_key]["total"] += 1
            lesson_stats[lesson_key]["attempts"] += result.attempts
            if result.passed:
                lesson_stats[lesson_key]["passed"] += 1
        
        # 生成分析报告
        analysis_parts = [
            f"## {student.name} 同学的学习情况分析\n\n",
            f"### 总体情况\n",
            f"- **总答题次数**: {total_attempts} 次\n",
            f"- **答题题目数**: {total_problems} 题\n",
            f"- **通过题目数**: {total_passed} 题\n",
            f"- **通过率**: {pass_rate}%\n\n"
        ]
        
        if lesson_stats:
            analysis_parts.append("### 各课程表现\n")
            for lesson, stats in lesson_stats.items():
                lesson_pass_rate = round((stats["passed"] / stats["total"] * 100) if stats["total"] > 0 else 0, 2)
                analysis_parts.append(
                    f"- **{lesson}**: 完成 {stats['total']} 题，通过 {stats['passed']} 题，"
                    f"通过率 {lesson_pass_rate}%，平均尝试次数 {round(stats['attempts'] / stats['total'], 1) if stats['total'] > 0 else 0} 次\n"
                )
            analysis_parts.append("\n")
        
        # 学习建议
        analysis_parts.append("### 学习建议\n")
        if pass_rate >= 80:
            analysis_parts.append("- 表现优秀！继续保持良好的学习状态。\n")
            analysis_parts.append("- 可以尝试挑战更高难度的题目。\n")
        elif pass_rate >= 60:
            analysis_parts.append("- 学习状态良好，但仍有提升空间。\n")
            analysis_parts.append("- 建议多复习已完成的题目，巩固基础知识。\n")
        else:
            analysis_parts.append("- 需要加强练习，建议多花时间在基础题目上。\n")
            analysis_parts.append("- 遇到困难时，可以查看参考答案或向老师请教。\n")
        
        if total_attempts / total_problems > 3 if total_problems > 0 else False:
            analysis_parts.append("- 部分题目尝试次数较多，建议仔细阅读题目要求，理清思路后再提交。\n")
        
        analysis = "".join(analysis_parts)
        
        # 尝试调用AI服务（如果存在）
        try:
            from app.services.ai.tasks.analyze import analyze_student as analyze_impl
            ai_analysis = await analyze_impl(req.student_id, results, {
                "total_attempts": total_attempts,
                "total_passed": total_passed,
                "total_problems": total_problems,
                "pass_rate": pass_rate,
                "lesson_stats": lesson_stats
            })
            if ai_analysis:
                analysis = ai_analysis
        except ImportError:
            # 如果没有AI实现，使用基础分析
            pass
        except Exception as e:
            # AI分析失败，使用基础分析
            print(f"AI分析失败，使用基础分析: {e}")
        
        return ApiResponse.success(
            data={
                "student_id": req.student_id,
                "status": "ok",
                "analysis": analysis
            },
            message="分析完成"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")
