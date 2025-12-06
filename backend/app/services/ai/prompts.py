"""Prompt 管理：为不同场景构建提示词列表/字符串

提供：
- build_post_summary_prompt(post, comments)
- build_chat_prompt(history, user_message)

提示结构使用 messages 列表，符合常见 chat 接口格式：
    [ { 'role': 'system'|'user'|'assistant', 'content': '...' }, ... ]
"""
from typing import List, Dict


def build_post_summary_prompt(post: Dict, comments: List[Dict]) -> List[Dict]:
    """为帖子和其评论构建 summary 模式的 prompt 列表。

    post: 对象，至少包含 title, content, author, created_at 等可选字段
    comments: 评论列表，每项至少包含 author, content
    返回 messages 列表，首条为 system 指令，后面为 user 提供的上下文
    """
    system = {
        'role': 'system',
        'content': (
            '你是一个中文的文本摘要助手。接下来你会阅读一个帖子及其若干评论。'
            ' 请以简洁、清晰、面向高中生的中文进行总结。'
            ' 输出应为纯文本摘要，不包含任何元数据或格式化标签，只输出中文自然语言。'
            ' 首条回复必须是直接的总结内容，长度控制在 40-150 字之间，确保抓住要点。'
        )
    }

    user_lines = [f"帖子标题：{post.get('title','')}", f"发帖正文：{post.get('content','')}" ]
    if post.get('author'):
        user_lines.append(f"发帖人：{post.get('author')}")
    if post.get('created_at'):
        user_lines.append(f"发布时间：{post.get('created_at')}")

    if comments:
        user_lines.append('\n下面是部分评论：')
        for c in comments[:20]:
            author = c.get('author', '匿名')
            content = c.get('content', '')
            user_lines.append(f"- {author}: {content}")

    user = {
        'role': 'user',
        'content': '\n'.join(user_lines)
    }

    return [system, user]


def build_chat_prompt(history: List[Dict], user_message: str) -> List[Dict]:
    """将已有对话历史（role/content）与当前用户消息拼成 messages 列表。

    history: list of {'role':'user'|'assistant', 'content': str}
    返回适用于 call_llm 的 messages 列表。
    """
    messages = []
    # 可加入一条通用 system 指令保证回答风格
    messages.append({
        'role': 'system',
        'content': '你是一个中文的助教型 AI，回答要友好、简洁、面向高中生，必要时给出示例或步骤。'
    })

    for h in (history or []):
        # 只允许 user/assistant 两种角色
        role = h.get('role') if isinstance(h, dict) else None
        content = h.get('content') if isinstance(h, dict) else str(h)
        if role in ('user', 'assistant'):
            messages.append({'role': role, 'content': content})

    # 最后追加当前用户消息
    messages.append({'role': 'user', 'content': user_message})
    return messages
"""
所有prompt模板集中管理
"""