"""
为提交代码的题目生成建议/反馈

导出函数:
- async def suggest_feedback(problem_id=None, problem_title='', problem_description='', code='') -> str

该函数构建 prompt 调用 LLM(client.call_llm)并返回纯文本建议。
"""
from typing import Optional, List, Dict
from app.services.ai.client import call_llm
from app.services.ai.prompts import build_feedback_prompt


async def suggest_feedback(problem_id: Optional[str] = None, problem_title: str = '', problem_description: str = '', code: str = '') -> str:
    """调用 LLM 生成针对提交代码的建议并返回文本。"""
    messages = build_feedback_prompt(problem_title or '', problem_description or '', code or '')
    # 低温度以提高稳定性
    reply = await call_llm(messages, temperature=0.2)
    if not isinstance(reply, str):
        reply = str(reply)
    return reply.strip()