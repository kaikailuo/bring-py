"""
题目管理相关API
"""
import os
import json
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.utils.security import get_current_active_user
from app.models.user import User
from app.models.student_result import StudentResult
from sqlalchemy.sql import func
from pydantic import BaseModel

# 引入服务层
from app.services.problems_service import (
    get_courses as svc_get_courses,
    get_course_problems as svc_get_course_problems,
    get_problem_markdown_path as svc_get_problem_markdown_path,
    get_problem_solution_path as svc_get_problem_solution_path,
    mock_run_code as svc_mock_run_code,
    mock_submit_code as svc_mock_submit_code,
)

router = APIRouter(prefix="/problems", tags=["题目管理"])


DATA_DIR = os.path.join(os.path.dirname(__file__), "../../../data/problems")  # 指向 problems 文件夹

@router.get("/index", summary="获取题目索引")
async def get_problem_index():
    """
    返回 index.json 内容
    """
    index_path = os.path.join(DATA_DIR, "index.json")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="index.json 未找到")
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)

@router.get("/{lesson}/{problem}/problem", summary="获取题目 Markdown")
async def get_problem_markdown(lesson: str, problem: str):
    """
    读取指定题目的 problem.md 文件
    """
    md_path = os.path.join(DATA_DIR, lesson, problem, "README.md")
    if not os.path.exists(md_path):
        raise HTTPException(status_code=404, detail="题目文件未找到")
    return FileResponse(md_path, media_type="text/markdown")


@router.get("/{lesson}/{problem}/assets/{filepath:path}", summary="获取题目静态资源（图片/附件）")
async def get_problem_asset(lesson: str, problem: str, filepath: str):
    """
    返回题目目录下的静态资源文件（例如图片），路径为 DATA_DIR/lesson/problem/{filepath}
    """
    asset_path = os.path.join(DATA_DIR, lesson, problem, filepath)
    if not os.path.exists(asset_path):
        raise HTTPException(status_code=404, detail="资源未找到")
    return FileResponse(asset_path)

@router.get("/{lesson}/{problem}/solution", summary="获取题目参考答案")
async def get_problem_solution(lesson: str, problem: str):
    """
    读取指定题目的 solution.md 文件（如果有）
    """
    md_path = os.path.join(DATA_DIR, lesson, problem, "solution.md")
    if not os.path.exists(md_path):
        raise HTTPException(status_code=404, detail="参考答案未找到")
    return FileResponse(md_path, media_type="text/markdown")

class CodeExecutionRequest(BaseModel):
    code: str

@router.get("/courses", summary="获取所有课程")
async def get_courses():
    """返回课程列表（由服务层提供）"""
    courses = svc_get_courses()
    if not courses:
        raise HTTPException(status_code=404, detail="未找到任何课程")
    return {"courses": courses}

@router.get("/courses/{course_id}/problems", summary="获取课程下的题目")
async def get_course_problems(course_id: str):
    """
    返回指定课程的题目列表
    """
    problems = svc_get_course_problems(course_id)
    if not problems:
        raise HTTPException(status_code=404, detail="课程或题目未找到")
    return {"problems": problems}

@router.post("/{lesson}/{problem}/run", summary="运行代码")
async def run_code(lesson: str, problem: str, request: CodeExecutionRequest):
    """
    模拟运行代码并返回结果
    """
    return await svc_mock_run_code(lesson,problem,request.code)

@router.post("/{lesson}/{problem}/submit", summary="提交代码")
async def submit_code(lesson: str, problem: str, request: CodeExecutionRequest,
                      current_user: User = Depends(get_current_active_user),
                      db: Session = Depends(get_db)):
    """
    模拟提交代码并返回测评结果，并记录学生提交结果到数据库
    """
    res = await svc_mock_submit_code(lesson, problem, request.code)

    try:
        # 兼容返回格式：res 包含 total 和 passed（数量）
        total = int(res.get('total', 0))
        passed_count = int(res.get('passed', 0))
        overall_passed = False
        if total > 0:
            overall_passed = (passed_count >= total)

        # 更新或创建 StudentResult
        if current_user and current_user.id:
            existing = db.query(StudentResult).filter(
                StudentResult.student_id == current_user.id,
                StudentResult.lesson == lesson,
                StudentResult.problem == problem
            ).first()
            if existing:
                existing.attempts = (existing.attempts or 0) + 1
                # 如果已有通过记录，则保持 True，否则根据本次结果更新
                existing.passed = bool(existing.passed) or bool(overall_passed)
                existing.last_submitted_at = func.now()
            else:
                new = StudentResult(
                    student_id=current_user.id,
                    lesson=lesson,
                    problem=problem,
                    attempts=1,
                    passed=bool(overall_passed)
                )
                db.add(new)
            db.commit()
    except Exception:
        db.rollback()

    return res
