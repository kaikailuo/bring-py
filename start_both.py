"""
同时启动前端和后端的脚本
"""
import subprocess
import sys
import os
import time
import signal
from pathlib import Path

def start_backend():
    """启动后端服务"""
    backend_dir = Path(__file__).parent / "backend"
    print("🚀 启动后端服务...")
    return subprocess.Popen(
        [sys.executable, "start_server.py"],
        cwd=backend_dir,
        shell=True
    )

def start_frontend():
    """启动前端服务"""
    frontend_dir = Path(__file__).parent / "frontend"
    print("🚀 启动前端服务...")
    return subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        shell=True
    )

def main():
    """主函数"""
    print("🎯 高中信息技术教学平台 - 启动脚本")
    print("=" * 50)
    
    backend_process = None
    frontend_process = None
    
    try:
        # 启动后端
        backend_process = start_backend()
        time.sleep(3)  # 等待后端启动
        
        # 启动前端
        frontend_process = start_frontend()
        
        print("\n✅ 服务启动完成！")
        print("📖 后端API文档: http://localhost:8000/docs")
        print("🌐 前端应用: http://localhost:5173")
        print("🧪 登录测试页面: http://localhost:5173/test-login")
        print("\n按 Ctrl+C 停止所有服务")
        
        # 等待进程
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 正在停止服务...")
        
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
            
        print("✅ 所有服务已停止")

if __name__ == "__main__":
    main()
