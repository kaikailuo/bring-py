"""
学生学情分析任务
从数据库获取学生数据，构建分析提示词，调用LLM进行AI分析
"""
from sqlalchemy.orm import Session
from app.utils.database import SessionLocal
from app.models.user import User, UserRole
from app.models.student_result import StudentResult
from app.services.ai.client import call_llm
from app.services.ai.prompts import build_student_analysis_prompt


async def analyze_student(student_id: int) -> str:
    """
    分析学生的学习情况，返回AI生成的分析报告
    
    参数：
        student_id: 学生ID
    
    返回：
        AI生成的分析报告字符串（Markdown格式）
    
    异常：
        ValueError: 学生不存在或没有答题记录
        Exception: 数据库查询或LLM调用失败
    """
    # 获取数据库会话
    db: Session = SessionLocal()
    
    try:
        # 获取学生信息
        student = db.query(User).filter(
            User.id == student_id,
            User.role == UserRole.STUDENT
        ).first()
        
        if not student:
            raise ValueError(f"学生不存在: ID={student_id}")
        
        # 获取该学生的所有答题记录
        results = db.query(StudentResult).filter(
            StudentResult.student_id == student_id
        ).all()
        
        if not results:
            # 没有答题记录时返回提示
            return f"{student.name} 同学目前还没有答题记录，建议鼓励其开始练习。"
        
        # 统计答题数据
        stats = _calculate_student_stats(student.name, results)
        
        # 构建分析提示词
        messages = build_student_analysis_prompt(student.name, stats)
        
        # 调用LLM生成分析报告
        analysis = await call_llm(messages, temperature=0.7)
        
        return analysis
        
    finally:
        db.close()


def _calculate_student_stats(student_name: str, results: list) -> dict:
    """
    计算学生的答题统计数据
    
    参数：
        student_name: 学生名字
        results: StudentResult对象列表
    
    返回：
        包含统计数据的字典
    """
    total_attempts = sum(r.attempts for r in results)
    total_passed = sum(1 for r in results if r.passed)
    total_problems = len(set((r.lesson, r.problem) for r in results if r.lesson and r.problem))
    pass_rate = round((total_passed / total_problems * 100) if total_problems > 0 else 0, 2)
    
    # 按课程分组统计
    lesson_stats = {}
    for result in results:
        lesson_key = result.lesson or "未分类"
        if lesson_key not in lesson_stats:
            lesson_stats[lesson_key] = {
                "total": 0,
                "passed": 0,
                "attempts": 0
            }
        lesson_stats[lesson_key]["total"] += 1
        lesson_stats[lesson_key]["attempts"] += result.attempts
        if result.passed:
            lesson_stats[lesson_key]["passed"] += 1
    
    return {
        "total_attempts": total_attempts,
        "total_passed": total_passed,
        "total_problems": total_problems,
        "pass_rate": pass_rate,
        "lesson_stats": lesson_stats
    }
