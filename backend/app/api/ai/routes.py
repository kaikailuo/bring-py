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
