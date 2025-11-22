import os

BASE_DIR = "backend/data/problems"
NUM_CASES = 20  # 每个 test 目录需要创建的 .in/.out 数量

def ensure_test_dir(problem_path):
    """确保 problem_xx 下存在 test/ 目录，没有则创建。"""
    test_path = os.path.join(problem_path, "test")
    if not os.path.exists(test_path):
        os.makedirs(test_path)
        print(f"创建 test 目录：{test_path}")
    return test_path


def create_test_files(test_path):
    """在 test/ 目录创建 1~20 的 .in/.out 文件（不存在才创建）"""
    for i in range(1, NUM_CASES + 1):
        in_file = os.path.join(test_path, f"{i}.in")
        out_file = os.path.join(test_path, f"{i}.out")

        if not os.path.exists(in_file):
            open(in_file, "w", encoding="utf-8").close()

        if not os.path.exists(out_file):
            open(out_file, "w", encoding="utf-8").close()


def is_problem_dir(path):
    """
    判断是否是 problem_xx 目录：
    - 必须是目录
    - 名字必须以 problem 开头
    """
    name = os.path.basename(path)
    return os.path.isdir(path) and name.startswith("problem")


def scan_problems():
    """扫描 backend/data/problems 下所有 lesson_xx/problem_xx"""
    for lesson_name in os.listdir(BASE_DIR):
        lesson_path = os.path.join(BASE_DIR, lesson_name)

        # 跳过非文件夹
        if not os.path.isdir(lesson_path):
            continue

        # lesson_xx 下的子目录
        for item in os.listdir(lesson_path):
            problem_path = os.path.join(lesson_path, item)

            # 找到 problem_xx
            if is_problem_dir(problem_path):
                print(f"处理问题目录：{problem_path}")
                test_path = ensure_test_dir(problem_path)
                create_test_files(test_path)


if __name__ == "__main__":
    scan_problems()
    print("所有 test 目录的测例文件创建完毕！")
