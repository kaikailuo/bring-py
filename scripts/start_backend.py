# -*- coding: utf-8 -*-
import subprocess
import os
import sys

def main():
    """启动后端服务"""
    backend_dir = os.path.join("backend")
    print("🚀 启动后端服务...")
    return subprocess.run(
        [sys.executable, "start_server.py"],
        cwd=backend_dir,
        shell=True
    )

if __name__ == "__main__":
    main()