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
    from app.models.post import Post
    from app.models.comment import Comment
    from app.models.favorite import Favorite
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    # 创建默认账户（学生和教师）
    create_default_accounts()


def create_default_accounts():
    """
    创建默认账户：8 个学生、2 个老师

    规则：
    - username = "身份+序号"，如 student1, teacher1
    - password = "123456"
    - role = UserRole.STUDENT / UserRole.TEACHER
    - name = 一些中文名（非张三李四）
    - email = "序号@example.com"，学生使用 1-8，教师使用 9-10
    """
    from app.services.auth import AuthService
    from app.schemas.user import UserCreate
    from app.models.user import UserRole

    db = SessionLocal()
    try:
        auth_service = AuthService(db)

        # 学生账户（1-8）
        student_names = [
            "王怡然",
            "刘思源",
            "陈馨予",
            "赵明轩",
            "周婧涵",
            "胡雅楠",
            "侯子辰",
            "钱悦彤",
        ]

        for i in range(1, 9):
            username = f"student{i}"
            email = f"{i}@example.com"
            # 检查是否存在
            if auth_service.get_user_by_username(username) or auth_service.get_user_by_email(email):
                continue
            user_data = UserCreate(
                username=username,
                password="123456",
                role=UserRole.STUDENT,
                name=student_names[i-1],
                email=email
            )
            try:
                auth_service.create_user(user_data)
                print(f"已创建学生账户: {username}/123456")
            except Exception as e:
                print(f"创建学生 {username} 失败: {e}")

        # 教师账户（teacher1, teacher2），emails 9@example.com, 10@example.com
        teacher_names = ["李博文", "苏欣怡"]
        t_email_start = 9
        for j in range(1, 3):
            username = f"teacher{j}"
            email = f"{t_email_start + j - 1}@example.com"
            if auth_service.get_user_by_username(username) or auth_service.get_user_by_email(email):
                continue
            user_data = UserCreate(
                username=username,
                password="123456",
                role=UserRole.TEACHER,
                name=teacher_names[j-1],
                email=email
            )
            try:
                auth_service.create_user(user_data)
                print(f"已创建教师账户: {username}/123456")
            except Exception as e:
                print(f"创建教师 {username} 失败: {e}")

    except Exception as e:
        print(f"创建默认账户失败: {e}")
    finally:
        db.close()
