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


def build_student_analysis_prompt(student_name: str, stats: Dict) -> List[Dict]:
    """为学生学情分析构建 prompt 列表。
    
    student_name: 学生名字
    stats: 包含学生答题统计信息的字典，包括：
        - total_attempts: 总答题次数
        - total_passed: 通过题目数
        - total_problems: 答题题目数
        - pass_rate: 通过率百分比
        - lesson_stats: 按课程分组的统计信息
    返回 messages 列表
    """
    system = {
        'role': 'system',
        'content': (
            '你是一个教育分析助手，专门分析高中生的编程学习情况。'
            '接下来你会收到一个学生的答题统计数据。'
            '请根据这些数据，用友好、鼓励、专业的语气生成一份详细的学习分析报告。'
            '报告应该包括：(1) 总体学习情况评价；(2) 各课程表现分析；(3) 学习优势和不足；(4) 具体的改进建议和鼓励。'
            '使用 Markdown 格式，确保内容清晰易读，面向高中生和教师。'
        )
    }
    
    # 构建用户数据内容
    user_lines = [
        f"学生名字：{student_name}",
        f"\n## 答题统计数据\n",
        f"- 总答题次数：{stats.get('total_attempts', 0)} 次",
        f"- 答题题目数：{stats.get('total_problems', 0)} 题",
        f"- 通过题目数：{stats.get('total_passed', 0)} 题",
        f"- 通过率：{stats.get('pass_rate', 0)}%"
    ]
    
    # 添加按课程分组的统计
    lesson_stats = stats.get('lesson_stats', {})
    if lesson_stats:
        user_lines.append("\n## 各课程表现")
        for lesson, lesson_data in lesson_stats.items():
            passed = lesson_data.get('passed', 0)
            total = lesson_data.get('total', 0)
            attempts = lesson_data.get('attempts', 0)
            avg_attempts = round(attempts / total, 1) if total > 0 else 0
            lesson_pass_rate = round((passed / total * 100) if total > 0 else 0, 2)
            
            user_lines.append(
                f"- **{lesson}**：完成 {total} 题，通过 {passed} 题，"
                f"通过率 {lesson_pass_rate}%，平均尝试次数 {avg_attempts} 次"
            )
    
    user = {
        'role': 'user',
        'content': '\n'.join(user_lines)
    }
    
    return [system, user]