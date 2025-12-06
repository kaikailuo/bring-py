"""帖子总结任务

提供：async def summarize_post(post_id: int) -> str
"""
from typing import List
from app.services.ai.client import call_llm
from app.services.ai.prompts import build_post_summary_prompt
from app.utils.database import SessionLocal
from app.models.post import Post
from app.models.comment import Comment


async def summarize_post(post_id: int) -> str:
    """从数据库读取帖子与评论，构建 prompt，调用 LLM 并返回纯文本摘要。

    返回纯文本字符串（不包含元信息）。
    """
    db = SessionLocal()
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise ValueError(f'找不到 post id={post_id}')

        # 读取若干最新评论
        comments_q = db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.id.asc()).all()

        # 将对象转换为简单 dict 结构供 prompt 使用
        post_obj = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': getattr(post, 'author_name', None) or getattr(post, 'author_id', None),
        }

        comments = []
        for c in comments_q:
            comments.append({'author': getattr(c, 'author_name', None) or c.author_id, 'content': c.content})

    finally:
        db.close()

    messages = build_post_summary_prompt(post_obj, comments)

    # 调用 LLM（低温度以获得稳定摘要）
    summary = await call_llm(messages, temperature=0.2)

    # 保证返回纯文本且尽量精简
    if not isinstance(summary, str):
        summary = str(summary)
    summary = summary.strip()

    # 将 summary 注入 chat session 以便后续基于该帖继续对话
    try:
        from app.services.ai.tasks.chat import set_summary_for_post
        # 忽略可能的错误
        set_summary_for_post(post_id, summary)
    except Exception:
        pass

    return summary
"""
帖子总结/学情总结
"""