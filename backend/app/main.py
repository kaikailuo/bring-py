"""
FastAPI应用程序主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.auth.routes import router as auth_router
from app.api.post import router as post_router
from app.api.comment import router as comment_router
from app.api.favorite import router as favorite_router
from app.api.problems.routes import router as problems_router
from app.utils.database import init_db
import uvicorn

# 创建FastAPI应用实例
app = FastAPI(
    title="高中信息技术教学平台API",
    description="提供学生、教师和管理员功能的RESTful API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # 前端开发服务器地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router, prefix="/api")
app.include_router(post_router, prefix="/api")
app.include_router(comment_router, prefix="/api")
app.include_router(favorite_router, prefix="/api")

# 注册题目管理相关路由，统一由 main 统一加上 /api 前缀，router 内使用 /problems
app.include_router(problems_router, prefix="/api")

@app.get("/")
async def read_root():
    """
    根路径接口
    """
    return JSONResponse(content={
        "code": 200,
        "message": "欢迎使用高中信息技术教学平台API",
        "data": {
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    })


@app.get("/health")
async def health_check():
    """
    健康检查接口
    """
    return JSONResponse(content={
        "code": 200,
        "message": "服务运行正常",
        "data": {
            "status": "healthy",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    })


@app.on_event("startup")
async def startup_event():
    """
    应用启动事件
    """
    # 初始化数据库
    init_db()
    print("数据库初始化完成")


@app.on_event("shutdown")
async def shutdown_event():
    """
    应用关闭事件
    """
    print("应用正在关闭...")


# 全局异常处理器
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "code": 404,
            "message": "请求的资源不存在",
            "data": None
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )