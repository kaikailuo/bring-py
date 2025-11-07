"""
题目管理相关API
"""
import os
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from fastapi import Depends
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
    return await svc_mock_run_code(request.code)

@router.post("/{lesson}/{problem}/submit", summary="提交代码")
async def submit_code(lesson: str, problem: str, request: CodeExecutionRequest):
    """
    模拟提交代码并返回测评结果
    """
    return await svc_mock_submit_code(request.code)
