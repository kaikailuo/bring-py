import os

# 定义目录结构
structure = {
    "backend": {
        "app": {
            "api": {},
            "models": {},
            "schemas": {},
            "services": {},
            "utils": {},
        },
        "tests": {}
    }
}

# 生成文件夹的函数
def create_dirs(base_path, tree):
    for name, subtree in tree.items():
        path = os.path.join(base_path, name)
        os.makedirs(path, exist_ok=True)
        print(f"📁 Created: {path}")
        create_dirs(path, subtree)

# 创建 main.py 和 requirements.txt
def create_files():
    main_path = os.path.join("backend", "app", "main.py")
    with open(main_path, "w", encoding="utf-8") as f:
        f.write("""from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI backend!"}
""")
    print(f"✅ Created: {main_path}")

    req_path = os.path.join("backend", "requirements.txt")
    with open(req_path, "w", encoding="utf-8") as f:
        f.write("fastapi\nuvicorn\nsqlalchemy\npydantic\n")
    print(f"✅ Created: {req_path}")

if __name__ == "__main__":
    create_dirs(".", structure)
    create_files()
    print("\n🎉 Backend structure created successfully!")
