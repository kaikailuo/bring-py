"""简单的内存聊天会话管理与处理

提供：
- chat_sessions: 内存 dict 存储每个会话的 history
- async def handle_chat(message: str, post_id: int|None) -> str
- def set_summary_for_post(post_id, summary)
"""
from typing import Dict, List, Optional
from app.services.ai.client import call_llm
from app.services.ai.prompts import build_chat_prompt

# session_id -> history(list of {role, content})
chat_sessions: Dict[str, List[Dict]] = {}
MAX_HISTORY = 10


def _session_key_for(post_id: Optional[str] = None, mode: str = 'basic') -> str:
    """构建 session key，包含 mode 以实现不同功能间的完全隔离。

    key 格式示例： 'basic:default'、'summarize:post:123'、'feedback:post:lesson_01/problem_01'
    """
    base = f'{mode}:post:{post_id}' if post_id is not None else f'{mode}:default'
    return base


def clear_session(post_id: Optional[str] = None, mode: str = 'basic'):
    """清理指定 mode 与 post_id 的会话记录，用于退出时释放内存。"""
    key = _session_key_for(post_id, mode)
    if key in chat_sessions:
        del chat_sessions[key]


def set_summary_for_post(post_id: Optional[str], summary: str, mode: str = 'summarize'):
    """在指定 mode/帖子的会话中注入一条 assistant 消息作为初始上下文（summary）。"""
    key = _session_key_for(post_id, mode)
    h = chat_sessions.get(key, [])
    # 插入为第一条 assistant 历史
    h.append({'role': 'assistant', 'content': summary})
    # 限制长度
    chat_sessions[key] = h[-MAX_HISTORY:]


async def handle_chat(message: str, post_id: Optional[str] = None, mode: str = 'basic'):
    """处理用户消息：按 session 搜集历史，调用 LLM，并返回 AI 回复文本。

    mode 用于区分三类会话（'basic'、'summarize'、'feedback' 等），以避免历史混淆。
    """
    key = _session_key_for(post_id, mode)
    history = chat_sessions.get(key, [])

    # 将用户消息追加到 history（在调用之前保存 user 提问）
    history.append({'role': 'user', 'content': message})
    # 限制长度（保留最后 MAX_HISTORY 条）
    history = history[-MAX_HISTORY:]

    # 构建 messages
    messages = build_chat_prompt(history, message)

    # 调用 LLM（默认温度稍高以获得对话感）
    try:
        reply = await call_llm(messages, temperature=0.7)
    except Exception as e:
        # 如果 LLM 客户端不可用（例如未配置 API key）或调用失败，返回一个友好的回退回复，避免抛出 500
        try:
            # 尝试引用具体错误消息但不要泄露敏感信息
            err_msg = str(e)
        except Exception:
            err_msg = ''
        fallback = (
            "AI 服务暂不可用；这是自动回复：我已收到你的问题，"
            "请稍后重试或联系教师。" + (" 错误信息: " + err_msg if err_msg else '')
        )
        # 将回退回复追加到 history 并返回
        history.append({'role': 'assistant', 'content': fallback})
        chat_sessions[key] = history[-MAX_HISTORY:]
        return fallback

    # 将 ai 回复追加到 history 并保存
    history.append({'role': 'assistant', 'content': reply})
    chat_sessions[key] = history[-MAX_HISTORY:]

    return reply

"""
基本对话功能
"""