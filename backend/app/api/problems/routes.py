"""
题目管理相关API
"""
import os
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

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
