"""
题目相关业务逻辑服务层
放置和解析 `backend/data/problems` 下的数据、index.json 以及模拟的运行/提交逻辑
"""
import os
import json
import tempfile
import shutil
import subprocess
import asyncio
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


async def mock_run_code(lesson: str, problem: str,code: str) -> Dict:
    """运行单个样例（1.in / 1.out）。
    如果 index.json 中记录该题 `has_test` 为 False，则直接通过。
    否则查找 `DATA_DIR/{lesson}/{problem}/test/1.in` 与 `1.out`，执行用户代码并比较输出。
    返回字典包含结果、输出与可能的错误信息。
    """
    # 查找 index.json 中对应条目，检查 has_test 字段
    index = load_index()
    target_path = f"{lesson}/{problem}"
    has_test = True
    if index:
        for item in index:
            if isinstance(item, dict) and item.get("path") == target_path:
                # 如果明确标注为 False，表示无需测试
                if item.get("has_test") is False:
                    has_test = False
                break

    if not has_test:
        return {"status": "success", "passed": True, "result": "此题无需测试", "message": "无需测试，直接通过"}

    # 定位样例文件
    test_dir = os.path.join(DATA_DIR, lesson, problem, "test")
    in_path = os.path.join(test_dir, "1.in")
    out_path = os.path.join(test_dir, "1.out")
    if not os.path.exists(in_path) or not os.path.exists(out_path):
        return {"status": "error", "message": "样例文件 1.in/1.out 未找到"}

    try:
        with open(in_path, "r", encoding="utf-8") as f:
            input_data = f.read()
    except Exception as e:
        return {"status": "error", "message": f"无法读取输入样例: {e}"}

    try:
        with open(out_path, "r", encoding="utf-8") as f:
            expected = f.read()
    except Exception as e:
        return {"status": "error", "message": f"无法读取输出样例: {e}"}

    # 在线程中运行阻塞的子进程执行代码
    def _run(code_src: str, stdin_data: str, timeout: int = 5):
        workdir = tempfile.mkdtemp(prefix="run_")
        try:
            file_path = os.path.join(workdir, "main.py")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code_src)

            proc = subprocess.run([
                "python", file_path
            ], input=stdin_data.encode("utf-8"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)

            stdout = proc.stdout.decode("utf-8", errors="replace")
            stderr = proc.stderr.decode("utf-8", errors="replace")
            return proc.returncode, stdout, stderr, False
        except subprocess.TimeoutExpired:
            return -1, "", "Timeout", True
        except Exception as e:
            return -2, "", str(e), False
        finally:
            try:
                shutil.rmtree(workdir)
            except Exception:
                pass

    def _call_and_format():
        run_res = _run(code, input_data)
        formatted = _format_run_result(run_res, expected)
        # 构建符合前端期望的返回格式
        actual = formatted.get('output', '')
        exp = formatted.get('expected', '')
        passed = formatted.get('passed', False)
        entry = {
            "passed": passed,
            "input": input_data,
            "expected": exp,
            "actual": actual
        }
        if passed:
            result= "样例通过"
        else:
            result= "样例未通过"
        resp = {"status": formatted.get('status', 'success'), "output": actual, "result": result, "testResults": [entry]}
        if 'stderr' in formatted:
            resp['stderr'] = formatted['stderr']
        if 'error' in formatted:
            resp['error'] = formatted['error']
        return resp

    return await asyncio.to_thread(_call_and_format)


def _normalize_output(s: str) -> str:
    # 去除行尾空白并统一换行，再剔除前后空白
    lines = [line.rstrip() for line in s.strip().splitlines()]
    return "\n".join(lines).strip()


def _format_run_result(run_res, expected_raw: str) -> Dict:
    returncode, stdout, stderr, timed_out = run_res
    expected = _normalize_output(expected_raw)
    out_norm = _normalize_output(stdout)
    
    passed = out_norm == expected
    if passed:
        output_message = "样例通过"
    else:
        output_message = "样例未通过"
    if timed_out:
        return {"status": "timeout", "passed": False, "output": stdout, "expected": expected, "error": "执行超时"}
    if returncode == -2:
        return {"status": "error", "passed": False, "output": stdout, "expected": expected, "error": stderr}

    
    result = {"status": "success", "passed": passed, "output": stdout, "expected": expected}
    if stderr:
        result["stderr"] = stderr
    return result


async def mock_submit_code(lesson: str, problem: str, code: str) -> Dict:
    """提交：运行题目下的所有样例（按 test 下的 *.in/*.out 成对检测）。
    返回每个样例的结果与汇总通过数。
    """
    # 检查 index.json 是否标注无需测试
    index = load_index()
    target_path = f"{lesson}/{problem}"
    has_test = True
    if index:
        for item in index:
            if isinstance(item, dict) and item.get("path") == target_path:
                if item.get("has_test") is False:
                    has_test = False
                break

    if not has_test:
        return {"status": "success", "total": 0, "passed": 0, "result": "此题无需测试", "message": "无需测试，直接通过"}

    test_dir = os.path.join(DATA_DIR, lesson, problem, "test")
    if not os.path.exists(test_dir):
        return {"status": "error", "message": "测试目录未找到"}

    # 收集所有 *.in 文件（按文件名的数字顺序排序，避免字典序如 '10' < '6' 的问题）
    files = [f for f in os.listdir(test_dir) if f.endswith('.in')]
    def _sort_key(fname: str):
        base = os.path.splitext(fname)[0]
        try:
            return (0, int(base))
        except Exception:
            return (1, base)
    files.sort(key=_sort_key)
    if not files:
        return {"status": "error", "message": "未找到任何测试用例"}

    testResults = []
    passed_count = 0

    def _run_single(inp_path, out_path):
        try:
            with open(inp_path, 'r', encoding='utf-8') as f:
                stdin_data = f.read()
        except Exception as e:
            return {"error": f"无法读取输入: {e}", "passed": False}
        try:
            with open(out_path, 'r', encoding='utf-8') as f:
                expected_raw = f.read()
        except Exception as e:
            return {"error": f"无法读取期望输出: {e}", "passed": False}

        def _run(code_src: str, stdin_data: str, timeout: int = 5):
            workdir = tempfile.mkdtemp(prefix="submit_")
            try:
                file_path = os.path.join(workdir, "main.py")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code_src)

                proc = subprocess.run([
                    "python", file_path
                ], input=stdin_data.encode("utf-8"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)

                stdout = proc.stdout.decode("utf-8", errors="replace")
                stderr = proc.stderr.decode("utf-8", errors="replace")
                return proc.returncode, stdout, stderr, False
            except subprocess.TimeoutExpired:
                return -1, "", "Timeout", True
            except Exception as e:
                return -2, "", str(e), False
            finally:
                try:
                    shutil.rmtree(workdir)
                except Exception:
                    pass

        run_res = _run(code, stdin_data)
        formatted = _format_run_result(run_res, expected_raw)
        return formatted

    # 顺序执行每个样例（可以并行化，但为安全起见顺序执行）
    for infile in files:
        base = infile[:-3]
        inp_path = os.path.join(test_dir, infile)
        out_path = os.path.join(test_dir, f"{base}.out")
        if not os.path.exists(out_path):
            testResults.append({"test": base, "passed": False, "input": "", "expected": "", "actual": "", "error": "缺少对应的 .out 文件"})
            continue
        res = await asyncio.to_thread(lambda p=inp_path, q=out_path: _run_single(p, q))
        ok = res.get('passed', False)
        try:
            with open(inp_path, 'r', encoding='utf-8') as f:
                input_content = f.read()
        except Exception:
            input_content = ''

        actual = res.get('output', '')
        expected = res.get('expected', '')
        if ok:
            passed_count += 1
        entry = {"test": base, "passed": ok, "input": input_content, "expected": expected, "actual": actual}
        if 'stderr' in res:
            entry['stderr'] = res['stderr']
        if 'error' in res:
            entry['error'] = res['error']
        testResults.append(entry)

    # 构建简要 result 字段供旧前端兼容
    result_summary = f"通过 {passed_count}/{len(testResults)} 个用例"
    return {"status": "success", "total": len(testResults), "passed": passed_count, "result": result_summary, "testResults": testResults}
