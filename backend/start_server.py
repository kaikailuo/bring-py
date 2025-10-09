"""
服务器启动脚本
"""
import uvicorn
import sys
import os

# 添加项目根目录到Python路径
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
