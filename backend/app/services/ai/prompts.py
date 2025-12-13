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


def build_feedback_prompt(problem_title: str, problem_description: str, code: str) -> List[Dict]:
    """为提交代码生成建议的 prompt。

    返回 messages 列表，第一条为 system 指令，第二条为包含题面与代码的 user 内容。
    """
    system = {
        'role': 'system',
        'content': (
            '你是一个面向高中生的编程助教。对于用户提交的代码，请提供简洁、建设性的反馈：指出可能的错误或逻辑缺陷，给出改进建议，必要时给出示例修正代码片段，且不要泄露敏感信息。'
        )
    }

    user_lines = [f"题目：{problem_title}", f"题面：{problem_description}", '\n提交的代码：', code]
    user = {
        'role': 'user',
        'content': '\n'.join(user_lines)
    }

    return [system, user]


def build_problem_generation_prompt(description: str) -> List[Dict]:
    """为生成 README.md 和 solution.md 构建 prompt。"""

    system = {
        'role': 'system',
        'content': (
            '你是中文的编程题目与测评生成器。'
            ' 根据用户提供的简要描述，生成两个文件：README.md 与 solution.md。'
            ' 输出必须是一个单独的 JSON 对象且不要包含任何额外的说明文本。'
            ' JSON 的字段为: readme, solution。\n\n'

            '【重要约束（必须严格遵守）】\n'
            '1. 本题为“标准输入 / 标准输出”类型程序题，而不是函数题。\n'
            '2. solution 中【禁止】定义任何函数（不得出现 def 关键字）。\n'
            '3. solution 中【禁止】使用列表（list）、元组（tuple）、字典（dict）或任何集合结构来表示输入数据。\n'
            '4. 所有输入必须通过 input() 逐行读取，或通过 input().split() 读取空格分隔的原始文本。\n'
            '5. 程序应自上而下顺序执行，直接 print 输出结果。\n\n'

            '【输入流与终止条件约束（必须遵守）】'
            '1. 若题目涉及多行输入，必须在“输入格式”中明确说明输入的总行数，或在第一行给出一个明确的整数 n，表示后续需要读取的行数或数据项数量。'
            '2. 禁止使用“读到 EOF 为止”、“直到文件结束”、“直到输入结束”等不确定终止方式。'
            '3. 禁止使用 while True、for line in sys.stdin、sys.stdin.read() 等依赖隐式结束条件的写法。'
            '4. 禁止使用“以空行结束输入”、“输入若干行”等模糊描述。'
            '5. 每一次 input() 的调用都必须在题目描述中有明确对应说明。'
            '6. 若输入为多个数，必须明确说明它们是位于同一行（空格分隔）还是分布在多行。'
            '7. solution 中的输入读取逻辑，必须与 README.md 中“输入格式”的描述逐条一一对应，不得额外读取未说明的输入行。'
            
            '【关于可变长度输入的额外限制】'
            '8. 若问题逻辑上需要处理多组数据或多条记录，必须显式给出数量 n，不得使用“若干个”“多组”“多行”等模糊描述。'
            '9. 禁止将 input().split() 的结果整体赋值给变量用于后续循环处理。\
                若使用 input().split()，必须在同一行中立即解包为确定数量的变量，\
                例如：a, b = map(int, input().split())。'
            '10. 禁止在 solution 中通过构造 list / tuple / dict 来存储全部输入数据，应按题目逻辑逐项读取、逐项处理、直接输出结果。'

            'readme 字段内容须严格遵循以下结构（示例参照）：\n'
            '# <题目标题>\n\n'
            '### 题目描述\n\n'
            '<题目正文>\n\n'
            '### 输入格式\n'
            '<输入说明（明确说明每一行或每一项的含义）>\n\n'
            '### 输出格式\n'
            '<输出说明>\n\n'
            '### 输入样例\n'
            '```\n'
            '<样例输入：必须是原始输入文本，每一行对应一次 input()，'
            '如有多个数请用空格分隔，不得使用 Python 列表或 JSON 形式>\n'
            '```\n\n'
            '### 输出样例\n'
            '```\n'
            '<样例输出>\n'
            '```\n\n'
            '并确保样例输入输出能够被 solution 中的程序正确处理。'
        )
    }

    user = {
        'role': 'user',
        'content': (
            f'请根据下面的简要需求生成题面（README.md）与参考答案（solution.md）。\n'
            f'需求：{description}\n\n'
            '注意：\n'
            '1) README.md 必须包含标题、题目描述、输入格式、输出格式、输入样例与输出样例等小节。\n'
            '2) 输入样例必须是“真实可输入的文本格式”，不得出现 Python 列表、元组、JSON。\n'
            '3) solution 字段必须只包含【一个】Python 代码块（```python ... ```），'
            '代码中不得定义函数，不得使用 list / dict / tuple 表示输入。\n'
            '4) 程序必须通过 input() 读取输入，并使用 print 输出结果。\n'
            '5) 最终请严格返回 JSON 对象，不要输出额外文本或说明。'
        )
    }

    return [system, user]


def build_tests_generation_prompt(readme: str, solution: str, count: int = 20) -> List[Dict]:
    """为生成测试用例构建 prompt。

    要求返回 JSON：{"tests": [{"input": "...", "output": "..."}, ...]}。
    输入输出为原始文本（多行输入请用换行嵌入）。
    """
    system = {
        'role': 'system',
        'content': (
            '你是一个编程题目的测评用例生成器。'
            ' 根据给定的 README（题面）与参考答案，生成准确且覆盖性的测试用例。'
            ' 输出必须是一个 JSON 对象，字段名为 tests，其值为一个数组，数组元素为 {"input": "...", "output": "..."}。'
            f' 目标数量为 {count} 个。'
        )
    }

    user = {
        'role': 'user',
        'content': f'题目（README）：\n{readme}\n\n参考答案（solution）：\n{solution}\n\n请生成 {count} 个测试用例，严格以 JSON 格式返回。'
    }

    return [system, user]
"""
所有prompt模板集中管理
"""