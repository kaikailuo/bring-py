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
    """返回课程列表。
    优先读取 `courses.json`（若存在），格式为 [{id,name}]；
    否则从 `index.json` 或目录扫描中自动推断。
    """
    # 优先读取 courses.json（便于集中管理课程名称）
    courses_file = os.path.join(DATA_DIR, "courses.json")
    if os.path.exists(courses_file):
        try:
            with open(courses_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 简单验证
                if isinstance(data, list):
                    good = True
                    for it in data:
                        if not isinstance(it, dict) or 'id' not in it or 'name' not in it:
                            good = False
                            break
                    if good:
                        return data
        except Exception:
            # 若解析失败，继续回退逻辑
            pass

    data = load_index()
    courses_set = []  # 保持列表以保证顺序
    seen = set()
    if data:
        for item in data:
            path = item.get("path") if isinstance(item, dict) else None
            if path:
                parts = path.split("/")
                if parts:
                    cid = parts[0]
                    if cid not in seen:
                        seen.add(cid)
                        courses_set.append(cid)

    if not courses_set:
        # 目录扫描回退，按目录名排序
        if os.path.exists(DATA_DIR):
            for name in sorted(os.listdir(DATA_DIR)):
                if os.path.isdir(os.path.join(DATA_DIR, name)):
                    courses_set.append(name)

    # 将 id 转为友好名称，例如 lesson_01 -> 课程一
    def _to_name(cid: str) -> str:
        # 尝试解析数字部分
        import re
        m = re.search(r"(\d+)", cid)
        if m:
            try:
                n = int(m.group(1))
                chinese = ["零","一","二","三","四","五","六","七","八","九","十",
                           "十一","十二","十三","十四","十五","十六","十七","十八","十九","二十"]
                if 0 <= n < len(chinese):
                    return f"课程{chinese[n]}"
            except Exception:
                pass
        # 无法解析则直接返回原 id
        return cid

    return [{"id": cid, "name": _to_name(cid)} for cid in courses_set]


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


def create_problem(lesson: str, title: str, description: str = '', solution: str = '', tests: Optional[List[Dict]] = None) -> Dict:
    """在指定 lesson 下创建一个新的 problem_xx 目录，写入 README.md, solution.md, test/ 文件，并更新 index.json。
    tests: 可选列表，每项为 {'input': '...', 'output': '...'}
    返回新创建题目的元信息或错误信息。
    """
    # 确保 lesson 目录存在
    lesson_dir = os.path.join(DATA_DIR, lesson)
    try:
        os.makedirs(lesson_dir, exist_ok=True)
    except Exception as e:
        return {"status": "error", "message": f"无法创建课程目录: {e}"}

    # 找到下一个可用的 problem 编号（以两位数字格式）
    existing = [name for name in os.listdir(lesson_dir) if os.path.isdir(os.path.join(lesson_dir, name)) and name.startswith('problem_')]
    nums = []
    for n in existing:
        try:
            nums.append(int(n.split('_')[-1]))
        except Exception:
            pass
    next_num = max(nums) + 1 if nums else 1
    prob_dirname = f"problem_{next_num:02d}"
    prob_path = os.path.join(lesson_dir, prob_dirname)

    try:
        os.makedirs(prob_path, exist_ok=False)
    except FileExistsError:
        return {"status": "error", "message": "题目目录已存在"}
    except Exception as e:
        return {"status": "error", "message": f"无法创建题目目录: {e}"}

    # 写入 README.md 和 solution.md
    try:
        with open(os.path.join(prob_path, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(description or '')
        with open(os.path.join(prob_path, 'solution.md'), 'w', encoding='utf-8') as f:
            f.write(solution or '')
    except Exception as e:
        return {"status": "error", "message": f"无法写入题面或参考答案: {e}"}

    # 创建测试目录并写入测试文件（如果提供）
    test_dir = os.path.join(prob_path, 'test')
    try:
        os.makedirs(test_dir, exist_ok=True)
        if tests:
            for idx, t in enumerate(tests, start=1):
                in_path = os.path.join(test_dir, f"{idx}.in")
                out_path = os.path.join(test_dir, f"{idx}.out")
                with open(in_path, 'w', encoding='utf-8') as fi:
                    fi.write(t.get('input', ''))
                with open(out_path, 'w', encoding='utf-8') as fo:
                    fo.write(t.get('output', ''))
    except Exception as e:
        return {"status": "error", "message": f"无法写入测试用例: {e}"}

    # 更新 index.json
    index_path = os.path.join(DATA_DIR, 'index.json')
    try:
        index = []
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f) or []
        # 尝试从 lesson 名中解析数字
        lesson_num = None
        try:
            lesson_num = int(''.join(filter(str.isdigit, lesson)))
        except Exception:
            lesson_num = None
        prob_num = next_num
        entry = {
            "lesson": lesson_num if lesson_num is not None else lesson,
            "problem": prob_num,
            "title": title,
            "path": f"{lesson}/{prob_dirname}",
            "has_test": bool(tests)
        }
        index.append(entry)
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return {"status": "error", "message": f"无法更新 index.json: {e}"}

    return {"status": "success", "lesson": lesson, "problem": prob_dirname, "path": entry['path'], "title": title}


def delete_problem(lesson: str, problem: str) -> Dict:
    """删除指定的题目录，并从 index.json 中移除对应条目。"""
    prob_path = os.path.join(DATA_DIR, lesson, problem)
    if not os.path.exists(prob_path):
        return {"status": "error", "message": "题目目录不存在"}

    try:
        shutil.rmtree(prob_path)
    except Exception as e:
        return {"status": "error", "message": f"无法删除题目目录: {e}"}

    # 更新 index.json：删除 path 匹配的条目
    index_path = os.path.join(DATA_DIR, 'index.json')
    try:
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f) or []
            new_index = [it for it in index if not (isinstance(it, dict) and it.get('path') == f"{lesson}/{problem}")]
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump(new_index, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return {"status": "error", "message": f"无法更新 index.json: {e}"}

    return {"status": "success", "message": "已删除"}


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
