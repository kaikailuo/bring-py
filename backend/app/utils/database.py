"""
数据库配置和连接工具
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


def get_db():
    """
    获取数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    初始化数据库
    """
    # 导入所有模型以确保它们被注册
    from app.models.user import User
    from app.models.question import Question, QuestionCategory, QuestionReply, QuestionSummary
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    # 创建默认管理员账户
    create_default_admin()


def create_default_admin():
    """
    创建默认管理员账户
    """
    from app.services.auth import AuthService
    from app.schemas.user import UserCreate
    
    db = SessionLocal()
    try:
        # 检查是否已存在管理员账户
        auth_service = AuthService(db)
        admin_user = auth_service.get_user_by_username("admin")
        
        if not admin_user:
            # 创建默认管理员账户
            admin_data = UserCreate(
                username="admin",
                password="admin123",
                role="admin",
                name="系统管理员",
                email="admin@example.com"
            )
            auth_service.create_user(admin_data)
            print("默认管理员账户已创建: admin/admin123")
        
    except Exception as e:
        print(f"创建默认管理员账户失败: {e}")
    finally:
        db.close()
