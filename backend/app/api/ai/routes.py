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
    占位：接收帖子ID并触发 AI 总结任务。
    当前为占位实现：立即返回任务已接受的占位响应。
    真实实现应：将任务入队列/异步调用模型，或者同步返回生成结果。
    """
    # TODO: 将请求推入异步任务队列或调用 AI 服务进行实际生成
    placeholder_summary = None
    print(req.post_id)  # 调试输出
    return {
        'post_id': req.post_id,
        'status': 'accepted',
        'summary': placeholder_summary
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
