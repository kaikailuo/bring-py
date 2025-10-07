# -*- coding: utf-8 -*-

import subprocess
import os
import platform

def get_npm_cmd():
    """根据操作系统返回正确的 npm 命令"""
    if platform.system() == "Windows":
        return "npm.cmd"
    return "npm"

def main():
    frontend_path = os.path.join("frontend")
    print("启动前端...")
    subprocess.run(
        [get_npm_cmd(), "run", "dev"],
        cwd=frontend_path
    )

if __name__ == "__main__":
    main()
