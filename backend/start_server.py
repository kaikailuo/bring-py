"""
服务器启动脚本
"""
import uvicorn
import sys
import os

# 添加项目根目录到Python路径
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("正在启动高中信息技术教学平台API服务器...")
    print("API文档地址: http://localhost:8000/docs")
    print("按 Ctrl+C 停止服务器")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
