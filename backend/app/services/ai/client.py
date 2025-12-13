import os
import json
import httpx


TONGYI_API_URL = os.getenv(
    'TONGYI_API_URL',
    'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
)
TONGYI_API_KEY = os.getenv('TONGYI_API_KEY', '')


class AIClientError(RuntimeError):
    pass


async def call_llm(messages: list, temperature: float = 0.7,
                   model: str = "qwen3-max") -> str:
    """
    通义千问 DashScope HTTP 版本（OpenAI 兼容模式）
    返回 assistant 的文本内容
    """
    if not TONGYI_API_KEY:
        raise AIClientError('未配置 TONGYI_API_KEY，无法调用 LLM 接口')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {TONGYI_API_KEY}',
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": False
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(TONGYI_API_URL, headers=headers, json=payload)
        except Exception as e:
            raise AIClientError(f'调用 LLM HTTP 请求失败: {e}')

    if resp.status_code != 200:
        raise AIClientError(f'LLM 返回错误状态 {resp.status_code}: {resp.text}')

    try:
        data = resp.json()
    except Exception as e:
        raise AIClientError(f'解析 JSON 失败: {e}')

    # 主要字段（DashScope / OpenAI 兼容模式）
    try:
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        pass

    # 回退策略，尽可能找内容
    possible = [
        ("result", str),
        ("summary", str),
        ("text", str),
        ("message", str),
    ]
    for key, t in possible:
        if key in data and isinstance(data[key], t):
            return data[key].strip()

    # 最后 fallback：返回完整 JSON
    return json.dumps(data, ensure_ascii=False)
