import os
import re
import json
from collections import defaultdict

input_path = "backend/data/problems/oj.md"   # 源文件
output_root = "backend/data/problems"        # 输出根目录
index_path = os.path.join(output_root, "index.json")

with open(input_path, "r", encoding="utf-8") as f:
    text = f.read()

# 匹配所有例题块
pattern = r"(##\s*例题(\d+)-(\d+)[\s\S]*?)(?=##\s*例题|\Z)"
matches = re.findall(pattern, text)

index_data = []
lesson_counter = defaultdict(int)

for full_block, lesson_num, _ in matches:
    lesson_counter[lesson_num] += 1  # 在该课内部递增
    problem_in_lesson = lesson_counter[lesson_num]

    # 提取题目标题
    title_match = re.search(r"##\s*(例题\d+-\d+：.*)", full_block)
    title = title_match.group(1).strip() if title_match else f"例题{lesson_num}-{problem_in_lesson}"

    # 提取答案示例部分
    solution_match = re.search(r"###\s*答案示例\s*\n+```python([\s\S]*?)```", full_block)
    solution = solution_match.group(1).strip() if solution_match else ""

    # 提取输入输出样例
    input_match = re.search(r"###\s*输入样例\s*\n+```([\s\S]*?)```", full_block)
    output_match = re.search(r"###\s*输出样例\s*\n+```([\s\S]*?)```", full_block)
    input_sample = input_match.group(1).strip() if input_match else "（无输入）"
    output_sample = output_match.group(1).strip() if output_match else "（无输出）"

    # 删除样例、答案部分，保留题面
    problem_text = re.sub(r"###\s*(输入|输出)样例[\s\S]*?(?=###|$)", "", full_block)
    problem_text = re.sub(r"###\s*答案示例[\s\S]*", "", problem_text).strip()
    problem_text = re.sub(r"^#{1,2}\s*例题\d+-\d+：.*\n*", "", problem_text)

    # 构造输出路径
    lesson_dir = os.path.join(output_root, f"lesson_{int(lesson_num):02d}")
    problem_dir = os.path.join(lesson_dir, f"problem_{problem_in_lesson:02d}")
    os.makedirs(problem_dir, exist_ok=True)

    # 写 README.md
    readme_content = f"# {title}\n\n" \
                     f"{problem_text}\n\n" \
                     f"## 输入样例\n```\n{input_sample}\n```\n\n" \
                     f"## 输出样例\n```\n{output_sample}\n```"

    with open(os.path.join(problem_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)

    # 写 solution.md
    if solution:
        with open(os.path.join(problem_dir, "solution.md"), "w", encoding="utf-8") as f:
            f.write(
                f"## 答案示例\n\n" \
                f"```python\n{solution}\n```")

    # 记录 index.json
    index_data.append({
        "lesson": int(lesson_num),
        "problem": problem_in_lesson,
        "title": title,
        "path": f"lesson_{int(lesson_num):02d}/problem_{problem_in_lesson:02d}"
    })

    print(f"✅ 已生成 lesson_{lesson_num}/problem_{problem_in_lesson}")

# 写 index.json
index_data.sort(key=lambda x: (x["lesson"], x["problem"]))
with open(index_path, "w", encoding="utf-8") as f:
    json.dump(index_data, f, ensure_ascii=False, indent=2)

print("全部完成 ✅")
