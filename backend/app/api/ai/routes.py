from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
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
    # 导入已实现的 chat 处理器（必须存在）
    try:
        from app.services.ai.tasks.chat import handle_chat
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'未找到 chat 实现: {e}')

    try:
        # handle_chat 已为 async 函数，直接 await
        reply = await handle_chat(req.message, post_id=req.post_id)
        return { 'reply': reply }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AIAnalyzeStudentRequest(BaseModel):
    student_id: int


class AIAnalyzeStudentResponse(BaseModel):
    student_id: int
    status: str
    analysis: Optional[str] = None


@router.post('/analyze-student', response_model=ApiResponse, summary="AI分析学生答题情况")
async def analyze_student(
    req: AIAnalyzeStudentRequest,
    current_user: User = Depends(get_current_user)
):
    """
    AI分析学生答题情况（仅教师和管理员可访问）
    接收学生ID，调用逻辑层进行分析，返回AI生成的分析结果
    """
    try:
        # 检查权限
        if current_user.role not in (UserRole.TEACHER, UserRole.ADMIN):
            raise HTTPException(status_code=403, detail="无权访问此资源")
        
        # 导入逻辑层的分析函数
        from app.services.ai.tasks.analyze import analyze_student as analyze_impl
        
        # 调用逻辑层函数，只传入学生ID
        analysis = await analyze_impl(req.student_id)
        
        return ApiResponse.success(
            data={
                "student_id": req.student_id,
                "status": "ok",
                "analysis": analysis
            },
            message="分析完成"
        )
    except ValueError as e:
        # 学生不存在或其他业务逻辑错误
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")
