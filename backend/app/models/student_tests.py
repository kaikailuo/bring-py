"""
学生测试题数据读取模块
读取 backend/data/problems/index.json 并提供查询接口
"""
import json
import os
from typing import List, Dict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PROBLEMS_INDEX = os.path.join(BASE_DIR, 'data', 'problems', 'index.json')


def load_all_problems() -> List[Dict]:
    """加载所有题目索引（如果文件存在）"""
    try:
        with open(PROBLEMS_INDEX, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def get_tests_for_student(student_id: int) -> List[Dict]:
    """返回给定学生的测验/题目清单。
    当前实现为返回全量题目索引；后续可按学生记录筛选或扩展为查询数据库。
    """
    problems = load_all_problems()
    # TODO: 根据 student_id 做更细粒度的筛选（例如记录学生历史、分组等）
    return problems
