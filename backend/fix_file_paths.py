import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.resource import Resource
from app.utils.database import Base

# 获取当前文件所在目录的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取backend目录路径
BASE_DIR = os.path.dirname(current_file_path)

# 数据库配置
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"

# 创建数据库引擎和会话
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB_PATH_PREFIX 常量
DB_PATH_PREFIX = "uploads/"

# 修复函数
def fix_file_paths():
    db = SessionLocal()
    try:
        # 查询所有资源记录
        resources = db.query(Resource).all()
        
        for resource in resources:
            # 如果file_path是绝对路径，转换为相对路径
            if os.path.isabs(resource.file_path):
                # 获取文件名
                file_name = os.path.basename(resource.file_path)
                # 更新为相对路径
                resource.file_path = f"{DB_PATH_PREFIX}{file_name}"
                print(f"修复资源ID {resource.id} 的路径: {resource.file_path}")
        
        # 提交更改
        db.commit()
        print(f"成功修复了 {len(resources)} 条资源记录的路径")
    except Exception as e:
        print(f"修复过程中发生错误: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_file_paths()