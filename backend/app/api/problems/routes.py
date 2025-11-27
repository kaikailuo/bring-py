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
    create_problem as svc_create_problem,
    delete_problem as svc_delete_problem,
    create_course as svc_create_course,
    delete_course as svc_delete_course,
)
import asyncio

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


class CreateProblemRequest(BaseModel):
    title: str
    description: str = ''
    solution: str = ''
    tests: list = []
    resources: list = []


class CreateCourseRequest(BaseModel):
    id: str
    name: str

@router.get("/courses", summary="获取所有课程")
async def get_courses():
    """返回课程列表（由服务层提供）"""
    courses = svc_get_courses()
    if not courses:
        raise HTTPException(status_code=404, detail="未找到任何课程")
    return {"courses": courses}


@router.post("/courses/{course_id}/problems", summary="创建新题目（教师）")
async def create_problem_endpoint(course_id: str, request: CreateProblemRequest):
    # course_id 形如 lesson_02
    res = await asyncio.to_thread(svc_create_problem, course_id, request.title, request.description, request.solution, request.tests, request.resources)
    if res.get('status') != 'success':
        raise HTTPException(status_code=400, detail=res.get('message', '创建失败'))
    return res


@router.post('/courses', summary='创建课程（教师）')
async def create_course_endpoint(request: CreateCourseRequest):
    res = await asyncio.to_thread(svc_create_course, request.id, request.name)
    if res.get('status') != 'success':
        raise HTTPException(status_code=400, detail=res.get('message', '创建课程失败'))
    return res


@router.delete('/courses/{course_id}', summary='删除课程（教师）')
async def delete_course_endpoint(course_id: str):
    res = await asyncio.to_thread(svc_delete_course, course_id)
    if res.get('status') != 'success':
        raise HTTPException(status_code=400, detail=res.get('message', '删除课程失败'))
    return res


@router.delete("/{lesson}/{problem}", summary="删除题目（教师）")
async def delete_problem_endpoint(lesson: str, problem: str):
    res = await asyncio.to_thread(svc_delete_problem, lesson, problem)
    if res.get('status') != 'success':
        raise HTTPException(status_code=400, detail=res.get('message', '删除失败'))
    return res

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
async def submit_code(lesson: str, problem: str, request: CodeExecutionRequest):
    """
    模拟提交代码并返回测评结果
    """
    return await svc_mock_submit_code(lesson, problem, request.code)
