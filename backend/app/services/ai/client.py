"""AI LLM 客户端（通义千问 / DashScope HTTP 调用封装）

提供统一的异步调用函数：call_llm(messages, temperature)

注意：需要在环境变量中配置 `TONGYI_API_URL` 和 `TONGYI_API_KEY`。
可根据阿里云 DashScope 的实际 HTTP API 调整请求体字段。
"""
import os
import json
import httpx

TONGYI_API_URL = os.getenv('TONGYI_API_URL', 'https://api.example.com/llm')
TONGYI_API_KEY = os.getenv('TONGYI_API_KEY', '')


class AIClientError(RuntimeError):
    pass


async def call_llm(messages: list, temperature: float = 0.7) -> str:
    """调用底层 LLM，返回纯文本回复。

    messages: list of {role: 'system'|'user'|'assistant', content: str}
    temperature: float 控制采样

    返回：字符串（纯文本）或抛出 AIClientError
    """
    headers = {
        'Content-Type': 'application/json'
    }
    if TONGYI_API_KEY:
        headers['Authorization'] = f'Bearer {TONGYI_API_KEY}'

    payload = {
        # Payload fields below are generic — 根据具体厂商 API 可能需要调整
        'messages': messages,
        'temperature': temperature,
        'max_tokens': 1024,
        'stream': False
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(TONGYI_API_URL, headers=headers, json=payload)
        except Exception as e:
            raise AIClientError(f'调用 LLM HTTP 请求失败: {e}')

    if resp.status_code != 200:
        detail = None
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text
        raise AIClientError(f'LLM 返回错误状态 {resp.status_code}: {detail}')

    try:
        data = resp.json()
    except Exception as e:
        raise AIClientError(f'解析 LLM 返回结果失败: {e}')

    # 尝试从常见字段中提取文本回复（不同提供商字段不同）
    # 支持多种可能：data['result'], data['choices'][0]['content'], data['data'][0]['content'] 等
    # 优先返回第一个非空文本片段
    candidates = []
    if isinstance(data, dict):
        if 'summary' in data and isinstance(data['summary'], str):
            candidates.append(data['summary'])
        if 'result' in data:
            if isinstance(data['result'], str):
                candidates.append(data['result'])
            elif isinstance(data['result'], dict):
                # e.g., {'content': '...'}
                text = data['result'].get('content') if isinstance(data['result'], dict) else None
                if text:
                    candidates.append(text)
        if 'choices' in data and isinstance(data['choices'], list) and data['choices']:
            first = data['choices'][0]
            if isinstance(first, dict):
                text = first.get('text') or first.get('content') or first.get('message')
                if text:
                    candidates.append(text if isinstance(text, str) else json.dumps(text, ensure_ascii=False))
        if 'data' in data and isinstance(data['data'], list) and data['data']:
            first = data['data'][0]
            if isinstance(first, dict):
                text = first.get('text') or first.get('content')
                if text:
                    candidates.append(text)

    # 最后退回到整个 body 的 text 字段或 raw
    if not candidates:
        # 尝试读取 flat text
        text = None
        if isinstance(data, dict):
            text = data.get('text') or data.get('message')
        if not text:
            # as last resort, dump json
            text = json.dumps(data, ensure_ascii=False)
        candidates.append(text)

    # 返回第一个候选并确保是字符串
    reply = candidates[0]
    if not isinstance(reply, str):
        reply = str(reply)

    return reply.strip()
