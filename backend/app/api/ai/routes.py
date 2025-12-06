from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

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
