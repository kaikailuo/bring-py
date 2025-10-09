import subprocess
import os
import platform

def get_npm_cmd():
    return "npm.cmd" if platform.system() == "Windows" else "npm"

def main():
    # 后端
    backend_path = os.path.join("backend")
    print("启动后端 FastAPI...")
    backend_proc = subprocess.Popen(
        ["uvicorn", "app.main:app", "--reload", "--port", "5000"],
        cwd=backend_path
    )

    # 前端
    frontend_path = os.path.join("frontend")
    print("启动前端 Vue...")
    frontend_proc = subprocess.Popen(
        [get_npm_cmd(), "run", "dev"],
        cwd=frontend_path
    )

    # 等待两个进程结束（一般按 Ctrl+C 停止）
    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("收到中断信号，停止前后端服务...")
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == "__main__":
    main()
