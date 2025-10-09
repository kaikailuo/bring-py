# -*- coding: utf-8 -*-
import subprocess
import os

def main():
    backend_path = os.path.join("backend")
    print("启动后端")
    subprocess.run(
        ["uvicorn", "app.main:app", "--reload", "--port", "5000"],
        cwd=backend_path
    )

if __name__ == "__main__":
    main()