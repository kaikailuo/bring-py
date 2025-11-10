"""
题目相关业务逻辑服务层
放置和解析 `backend/data/problems` 下的数据、index.json 以及模拟的运行/提交逻辑
"""
import os
import json
from typing import List, Dict, Optional

BASE_DIR = os.path.dirname(__file__)
# 从 services 目录出发，回到 backend/data/problems
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../data/problems"))


def load_index() -> Optional[List[Dict]]:
    """加载 index.json，失败返回 None"""
    index_path = os.path.join(DATA_DIR, "index.json")
    if not os.path.exists(index_path):
        return None
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def get_courses() -> List[str]:
    """返回课程列表，优先使用 index.json 的 path 字段抽取课程名；回退到目录扫描"""
    data = load_index()
    courses_set = set()
    if data:
        for item in data:
            path = item.get("path") if isinstance(item, dict) else None
            if path:
                parts = path.split("/")
                if parts:
                    courses_set.add(parts[0])

    if not courses_set:
        # 目录扫描回退
        if os.path.exists(DATA_DIR):
            for name in os.listdir(DATA_DIR):
                if os.path.isdir(os.path.join(DATA_DIR, name)):
                    courses_set.add(name)

    return sorted(courses_set)


def get_course_problems(course_id: str) -> List[Dict]:
    """返回指定课程下的题目列表。优先从 index.json 中获取 title/path/problem 字段；否则目录扫描返回子目录名。"""
    data = load_index()
    problems = []
    if data:
        for item in data:
            path = item.get("path") if isinstance(item, dict) else None
            if path and path.startswith(f"{course_id}/"):
                # 尝试解析 problem 名称
                parts = path.split("/")
                prob = parts[1] if len(parts) > 1 else None
                problems.append({
                    "problem": prob,
                    "title": item.get("title"),
                    "path": path
                })
        if problems:
            return problems

    # 回退到目录扫描
    course_path = os.path.join(DATA_DIR, course_id)
    if not os.path.exists(course_path):
        return []
    for name in os.listdir(course_path):
        if os.path.isdir(os.path.join(course_path, name)):
            problems.append({"problem": name, "title": None, "path": f"{course_id}/{name}"})
    return problems


def get_problem_markdown_path(lesson: str, problem: str) -> Optional[str]:
    md_path = os.path.join(DATA_DIR, lesson, problem, "README.md")
    return md_path if os.path.exists(md_path) else None


def get_problem_solution_path(lesson: str, problem: str) -> Optional[str]:
    sol_path = os.path.join(DATA_DIR, lesson, problem, "solution.md")
    return sol_path if os.path.exists(sol_path) else None


async def mock_run_code(code: str) -> Dict:
    # 这里保留为异步接口以便未来替换成真正的评测器
    return {"status": "success", "output": "运行结果示例"}


async def mock_submit_code(code: str) -> Dict:
    return {"status": "success", "result": "通过所有测试用例"}
