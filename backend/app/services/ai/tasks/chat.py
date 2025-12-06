"""简单的内存聊天会话管理与处理

提供：
- chat_sessions: 内存 dict 存储每个会话的 history
- async def handle_chat(message: str, post_id: int|None) -> str
- def set_summary_for_post(post_id, summary)
"""
from typing import Dict, List
from app.services.ai.client import call_llm
from app.services.ai.prompts import build_chat_prompt

# session_id -> history(list of {role, content})
chat_sessions: Dict[str, List[Dict]] = {}
MAX_HISTORY = 10


def _session_key_for(post_id: int | None) -> str:
    return f'post:{post_id}' if post_id is not None else 'default'


def set_summary_for_post(post_id: int, summary: str):
    """在指定帖子的会话中注入一条 assistant 消息作为初始上下文（summary）。"""
    key = _session_key_for(post_id)
    h = chat_sessions.get(key, [])
    # 插入为第一条 assistant 历史
    h.append({'role': 'assistant', 'content': summary})
    # 限制长度
    chat_sessions[key] = h[-MAX_HISTORY:]


async def handle_chat(message: str, post_id: int | None):
    """处理用户消息：按 session 搜集历史，调用 LLM，并返回 AI 回复文本。"""
    key = _session_key_for(post_id)
    history = chat_sessions.get(key, [])

    # 将用户消息追加到 history（在调用之前保存 user 提问）
    history.append({'role': 'user', 'content': message})
    # 限制长度（保留最后 MAX_HISTORY 条）
    history = history[-MAX_HISTORY:]

    # 构建 messages
    messages = build_chat_prompt(history, message)

    # 调用 LLM（默认温度稍高以获得对话感）
    reply = await call_llm(messages, temperature=0.7)

    # 将 ai 回复追加到 history 并保存
    history.append({'role': 'assistant', 'content': reply})
    chat_sessions[key] = history[-MAX_HISTORY:]

    return reply
"""
基本对话功能
"""